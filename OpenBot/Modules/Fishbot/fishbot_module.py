from OpenBot.Modules.Actions import ActionFunctions, ActionBotInterface
from OpenBot.Modules import OpenLib, Dropper
import ui, item, player, net, chat, app, chr
import eXLib

STATES = {
    'STOPPED': 0,
    'STARTED': 1,
    'FISHING': 2,
    'OPENING_FISH': 3,
    'BUYING_BAIT': 4,
    'FRYING_FISH': 5,
    'IMPROVING_ROD': 6,
    'SELLING_CATCHES': 7,
    'ADDING_THINGS_TO_DROPPER': 8,
}

CAMPFIRE_ID = 27600
CAMPFIRE_RACE = 12000

class Fishbot(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.enabled = False
        self.grill_fish = True
        self.instant_fishing = False
        self.is_rod_down = True
        self.check_repetitions = False
        self.repetitions = 0
        self.max_repetitions = 0
        self.time_between_fishing = 0
        self.min_time_between_fish = 5
        self.max_time_between_fish = 10
        self.starting_position = (0, 0)  # X, Y
        self.currState = STATES['STARTED']
        # KEY - FISH ID, VALUE - DEAD FISH ID
        self.fish = {
            27803: 27833,
            27804: 27834,
            27805: 27835,
            27806: 27836,
            27807: 27837,
            27808: 27838,
            27809: 27839,
            27810: 27840,
            27811: 27841,
            27812: 27842,
            27813: 27843,
            27814: 27844,
            27815: 27845,
            27816: 27845,
            27817: 27847,
            27818: 27848,
            27819: 27849,
            27820: 27850,
            27821: 27851,
            27822: 27852,
            27823: 27853,
            27824: 27854,
            27825: 27855,
            27826: 27856,
            27827: 27857,
            27828: 27858,
            27829: 27859,
            27830: 27860,
            27831: 27861,
            27832: 27862,
            27987: 27990,
        }
        # KEY - BAIT ID, VALUE - SLOT IN FISHERMAN SHOP
        self.baits = {
            27798: -1,
            27800: -1,
            27802: -1,
            27801: 7,
        }
        # KEY - NAME, VALUE - CATCHES ID
        self.catches = {'FUGITIVES_CAPE': 70048,
            'SAGE_KINGS_GLOVE': 70051,
            'SAGE_KINGS_SYMBOL': 70050,
            'LUCYS_RING': 70049,
            'GOLD_RING': 50002,
            'GOLD_PIECE': 80008,
            'GOLD_KEY': 50008,
            'SILVER_KEY': 50009,
            'MERMAID_KEY': 50043,
            'BLEACH': 70201,
            'BLONDE_HAIR_DYE': 70203,
            'BROWN_HAIR_DYE': 70205,
            'RED_HAIR_DYE': 70204,
            'BLACK_HAIR_DYE': 70206,
            'WHITE_HAIR_DYE': 70202,
        }
        self.catches_to_drop = []
        self.catches_to_sell = []
        self.fish_id_to_open = []
        self.dead_fish_id_to_grill = []
        self.dead_fish_it_to_drop = []
        self.lastActionDone = True
        self.lastTimeUpdated = 0
        self.lastTimeFishing = 0
        self.lastTimeWaiting = 0
        self.lastTImeBetweenWaiting = 0
        self.waitBetweenFishing = False
        self.minTimeBetweenFish = 0
        self.maxTimeBetweenFish = 1

    def start(self):
        self.enabled = True
        self.currState = STATES['STARTED']
        eXLib.BlockFishingPackets()
        x, y, z = player.GetMainCharacterPosition()
        self.starting_position = (x, y)

    def stop(self):
        self.repetitions = 0
        self.enabled = False
        self.currState = STATES['STOPPED']
        self.pull_rod()
        eXLib.SendStopFishing(eXLib.UNSUCCESS_FISHING, 0)
        eXLib.UnblockFishingPackets()
        chat.AppendChat(3, 'Stop')

    def switch_instant_fish(self):
        if self.instant_fishing:
            self.instant_fishing = False
            eXLib.RecvStartFishCallback(0)
        else:
            self.instant_fishing = True
            eXLib.RecvStartFishCallback(self.pull_rod)

    def action_done_callback(self):
        self.lastActionDone = True

    def check_rod(self):
        # Check if rod is available
        val = OpenLib.isItemTypeOnSlot(item.ITEM_TYPE_ROD, player.EQUIPMENT, item.EQUIPMENT_WEAPON)
        if val:
            return True

        slot = OpenLib.GetItemByType(item.ITEM_TYPE_ROD)
        if slot == -1:
            chat.AppendChat(3, "[Fishing-Bot] No rod available, you need a rod first")
            self.stop()
            return False

        if not self.can_improve_rod():
            net.SendItemUsePacket(slot)
        return False

    @staticmethod
    def can_improve_rod():
        idx = player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WEAPON)
        if idx:
            item.SelectItem(idx)
            curr_points = player.GetItemMetinSocket(player.EQUIPMENT, item.EQUIPMENT_WEAPON, 0)
            max_points = item.GetValue(2)

            if curr_points == max_points and item.GetItemType() == item.ITEM_TYPE_ROD:
                chat.AppendChat(3, "[Fishing-Bot] Rod is ready to be upgraded.")
                return True

        return False

    def check_bait(self):
        for bait in self.baits.keys():
            if OpenLib.GetItemByID(bait) >= 0:
                return True
        return False

    def pull_rod(self):
        self.is_rod_down = True
        eXLib.SendStopFishing(eXLib.SUCCESS_FISHING, app.GetRandom(3, 10))
        self.currState = STATES['ADDING_THINGS_TO_DROPPER']
        self.repetitions += 1

    @staticmethod
    def get_campfire_vid():
        for vid in eXLib.InstancesList:
            chr.SelectInstance(vid)
            if chr.GetRace() == CAMPFIRE_RACE:
                return vid
        return 0

    def OnUpdate(self):
        can_update, self.lastTimeUpdated = OpenLib.timeSleep(self.lastTimeUpdated, 0.05)
        if self.enabled and can_update and self.lastActionDone and OpenLib.IsInGamePhase():

            if self.currState == STATES['STOPPED']:
                chat.AppendChat(3, 'Stopped state')
                val, self.lastTimeWaiting = OpenLib.timeSleep(self.lastTimeWaiting,
                                                              app.GetRandom(self.minTimeBetweenfish,
                                                                            self.maxTimeBetweenfish))
                if val:
                    self.currState = STATES['STARTED']
                return

            elif self.currState == STATES['STARTED']:
                #chat.AppendChat(3, 'Started')
                if OpenLib.isInventoryFull():
                    chat.AppendChat(3, 'Inventory is full')
                    self.stop()

                if self.check_repetitions:
                    if self.repetitions >= self.max_repetitions:
                        self.stop()

                if not self.check_rod():
                    # If in this round character is wearing rod,
                    # bot will be not stopped,
                    # otherwise, if character do not have a rod, bot is stopping
                    return

                if self.can_improve_rod():
                    self.currState = STATES['IMPROVING_ROD']
                    net.SendItemUsePacket(player.EQUIPMENT, item.EQUIPMENT_WEAPON)
                    #chat.AppendChat(3, 'Going to improve rod')
                    return

                if not self.check_bait():
                    self.currState = STATES['BUYING_BAIT']
                    #chat.AppendChat(3, 'Going to buy some bait')
                    return

                x, y = self.starting_position
                if not OpenLib.isPlayerCloseToPosition(x, y, max_dist=300):
                    # Go to starting position
                    #chat.AppendChat(3, 'Going to starting position')
                    action = {
                        'name': '[Fishbot] - Going to start position',
                        'function_args': [self.starting_position],
                        'function': ActionFunctions.MoveToPosition,
                        'callback': self.action_done_callback,
                    }
                    self.lastActionDone = False
                    ActionBotInterface.action_bot_interface.AddAction(action)
                    return

                self.currState = STATES['FISHING']

            elif self.currState == STATES['FISHING']:
                if self.is_rod_down:
                    for key in [27802, 27800, 27798, 27801]:
                        #chat.AppendChat(3, str(key))
                        slot = OpenLib.GetItemByID(key)
                        if slot > -1:
                            net.SendItemUsePacket(slot)
                            break
                    eXLib.SendStartFishing(2)
                    self.is_rod_down = False
                    return

                # eXLib.RecvStartFishCallback is taking care of instant fishing
                if not self.instant_fishing:
                    if not self.time_between_fishing:
                        self.time_between_fishing = app.GetRandom(self.min_time_between_fish,
                                                                  self.max_time_between_fish)

                    val_can_fish, self.lastTimeFishing = OpenLib.timeSleep(self.lastTimeFishing,
                                                                           self.time_between_fishing)
                    if val_can_fish:
                        self.time_between_fishing = 0
                        self.pull_rod()

            elif self.currState == STATES['ADDING_THINGS_TO_DROPPER']:
                # Opening fish
                fish_to_open = OpenLib.GetItemsSlotsByID(self.fish_id_to_open)
                for slots in fish_to_open.values():
                    for slot in slots:
                        net.SendItemUsePacket(slot)

                # Dropping fish
                fish_to_drop = OpenLib.GetItemsSlotsByID(self.dead_fish_it_to_drop)
                for slots in fish_to_drop.values():
                    for slot in slots:
                        if player.GetItemCount(slot < 200):
                            continue
                        Dropper.dropper.add_new_item_to_drop(slot)

                # Dropping catches
                catches_to_drop = OpenLib.GetItemsSlotsByID(self.catches_to_drop)
                for slots in catches_to_drop.values():
                    for slot in slots:
                        Dropper.dropper.add_new_item_to_drop(slot)
                self.currState = STATES['OPENING_FISH']
                return

            elif self.currState == STATES['OPENING_FISH']:

                fish_to_drop = OpenLib.GetItemsSlotsByID(self.dead_fish_it_to_drop)
                catches_to_drop = OpenLib.GetItemsSlotsByID(self.catches_to_drop)

                if not OpenLib.DoPlayerHasItems(fish_to_drop) and not OpenLib.DoPlayerHasItems(catches_to_drop):
                    self.currState = STATES['STARTED']
                    return

                excluded_fish_to_drop = Dropper.dropper.is_item_slot_in_chosen_items_list(fish_to_drop, Dropper.dropper.items_slots_to_drop)
                excluded_catches_to_drop = Dropper.dropper.is_item_slot_in_chosen_items_list(catches_to_drop, Dropper.dropper.items_slots_to_drop)

                if excluded_fish_to_drop:
                    for slot in excluded_fish_to_drop:
                        Dropper.dropper.add_new_item_to_drop(slot)

                if excluded_catches_to_drop:
                    for slot in excluded_catches_to_drop:
                        Dropper.dropper.add_new_item_to_drop(slot)

                return

            elif self.currState == STATES['BUYING_BAIT']:
                action = {
                    'name': '[Fishbot] - Buying bait',
                    'function_args': [[7, 7, 7, 7], 9009, [1], self.action_done_callback],
                    'function': ActionFunctions.GoBuyItemsFromNPC,
                }
                self.pull_rod()
                self.currState = STATES['SELLING_CATCHES']
                self.lastActionDone = False
                ActionBotInterface.action_bot_interface.AddAction(action)
                return

            elif self.currState == STATES['FRYING_FISH']:
                chat.AppendChat(3, 'Frying fish')
                if not self.should_character_grill_fish():
                    self.currState = STATES['STARTED']
                    return

                if self.grill_fish:
                    campfire_vid = self.get_campfire_vid()
                    if campfire_vid:
                        chat.AppendChat(3, 'Grilling')
                        action = {
                            'name': '[Fishbot] - Grill fish',
                            'function_args': [self.dead_fish_id_to_grill, campfire_vid],
                            'function': ActionFunctions.GrillFish,
                            'callback': self.action_done_callback,
                        }
                        self.currState = STATES['STARTED']
                        self.lastActionDone = False
                        ActionBotInterface.action_bot_interface.AddAction(action)
                        return
                    else:
                        chat.AppendChat(3, 'Campfire is not setted')
                        if OpenLib.GetItemByID(CAMPFIRE_ID) >= 0:
                            OpenLib.UseAnyItemByID([CAMPFIRE_ID])
                            chat.AppendChat(3, 'Use camprife')
                            return

                        chat.AppendChat(3, 'Buying campfire')
                        action = {
                            'name': '[Fishbot] - Buying campfire',
                            'function_args': [[1], 9009, [1], self.action_done_callback],
                            'function': ActionFunctions.GoBuyItemsFromNPC,
                        }
                        self.lastActionDone = False
                        ActionBotInterface.action_bot_interface.AddAction(action)
                        return

                self.currState = STATES['STARTED']

            elif self.currState == STATES['IMPROVING_ROD']:
                action = {
                    'name': '[Fishbot] - Upgrading rod',
                    'function_args': [0],
                    'function': ActionFunctions.ImproveRod,
                    'callback': self.action_done_callback,
                }
                self.lastActionDone = False
                self.currState = STATES['STARTED']
                ActionBotInterface.action_bot_interface.AddAction(action)
                return

            elif self.currState == STATES['SELLING_CATCHES']:
                slots_to_sell = []
                for slots in OpenLib.GetItemsSlotsByID(self.catches_to_sell).values():
                    slots_to_sell += slots

                if slots_to_sell:
                    action = {
                        'name': '[Fishbot] - Selling items',
                        'function_args': [slots_to_sell, 9009, [1], self.action_done_callback],
                        'function': ActionFunctions.GoSellItemsToNPC,
                    }
                    self.lastActionDone = False
                    #chat.AppendChat(3, 'Selling ' + str(slots_to_sell))
                    ActionBotInterface.action_bot_interface.AddAction(action)

                self.currState = STATES['FRYING_FISH']
                return

    def should_character_grill_fish(self):
        fish_to_grill = OpenLib.GetItemsSlotsByID(self.dead_fish_id_to_grill)
        for items in fish_to_grill.values():
            if items:
                return True
        return False


fishbot_module = Fishbot()
fishbot_module.Show()
