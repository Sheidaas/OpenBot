from time import sleep, time
from OpenBot.Modules import MapManager, Movement, OpenLib
from OpenBot.Modules import OpenLog
from OpenBot.Modules.Actions import ActionBot, ActionRequirementsCheckers
from OpenBot.Modules import NPCInteraction
from OpenBot.Modules.NPCInteraction import NPCAction
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import Hooks
import eXLib
import player, net, chr, chat, background, item


def ClearFloor(args):
    player.SetAttackKeyState(False)
    x, y = args[0]
    my_x,my_y, z = player.GetMainCharacterPosition()
    path = eXLib.FindPath(my_x,my_y,x,y)
    if not path:
        return True
    is_monster_nearby = OpenLib.IsMonsterNearby()
    if OpenLib.isPlayerCloseToPosition(x, y) and not is_monster_nearby:
        return True

    if not is_monster_nearby:
        action_dict = {'args': [(x, y)], # position
        'function': MoveToPosition,
        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (x, y)},
        'on_failed': [ActionBot.NEXT_ACTION],
        }
        return action_dict

    #if len(args) > 1:
    #    interruptors = args[1]
    #    for interruptor in interruptors:
    #        if interruptor():
    #            return False


    vid = OpenLib.GetNearestMonsterVid()
    action_dict = {'args': [0, vid], # position
    'function': Destroy,
    'requirements': {},
    'on_success': [ActionBot.NEXT_ACTION],
    }
    return action_dict

def Destroy(args):
    if args[1]:
        instance_vid = args[1]
    else:
        instance_vid = 0
        for vid in eXLib.InstancesList:
            chr.SelectInstance(vid)
            if chr.GetRace() == args[0]:
                instance_vid = vid
                break

    if eXLib.IsDead(instance_vid):
        player.SetAttackKeyState(False)
        return True

    vid_life_status = OpenLib.AttackTarget(instance_vid)

    if vid_life_status == OpenLib.TARGET_IS_DEAD:
        player.SetAttackKeyState(False)
        return True

    elif vid_life_status == OpenLib.ATTACKING_TARGET:
        return False

    elif vid_life_status == OpenLib.MOVING_TO_TARGET:
        return False
    
    return False

def Find(args):
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if chr.GetRace() == args[0]:
            return True
    return False

def MoveToPosition(args):
    position = args[0]
    if OpenLib.isPlayerCloseToPosition(position[0], position[1]):
        return True
    if len(args) > 1:
        error = Movement.GoToPositionAvoidingObjects(position[0], position[1], mapName=args[1])
    else:
        error = Movement.GoToPositionAvoidingObjects(position[0], position[1], mapName=background.GetCurrentMapName())

    if error != None:
        return True
    return False

def MoveToVID(args):
    x, y, z = chr.GetPixelPosition(args[0])
    return MoveToPosition([(x, y)])

def UsingItemOnInstance(args):
    instance = args[0]
    item_slot = args[1]
    if OpenLib.isPlayerCloseToInstance(instance):
        net.SendGiveItemPacket(instance, player.SLOT_TYPE_INVENTORY, item_slot, player.GetItemCount(item_slot))
        OpenLib.skipAnswers([0, 0], True)
        return True

    x, y, z = chr.GetPixelPosition(instance)
    action_dict = {'args': [(x, y)], # position
                    'function': MoveToPosition,
                    'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (x, y)},
                    'on_failed': [ActionBot.NEXT_ACTION],
                    }
    return action_dict

def OpenAllSeals(args): # center position of floor, 
    #DebugPrint('Launch OpenAllSeals')
    closest_seal = OpenLib.getClosestInstance([OpenLib.OBJECT_TYPE])
    #DebugPrint('Closest seal ' + str(closest_seal))
    if closest_seal < 0:
        #DebugPrint('There is no seal to open')
        return True

    slot_with_key = OpenLib.GetItemByID(50084)
    if slot_with_key >= 0:
        #DebugPrint('Char has an stone key')
        #DebugPrint('Using item on seal')
        action_dict = {'args': [closest_seal, slot_with_key], # position
                        'function': UsingItemOnInstance,
                        'requirements': {},
                        'on_success': [ActionBot.NEXT_ACTION],
                        'on_failed': [ActionBot.NEXT_ACTION],
                        }
        return action_dict
        


    x, y = args[0]
    #DebugPrint('Clearing the floor')
    action_dict = { 'args': [(x, y), [_returnHasItemInterruptorWithArgs(50084)]], # center position of area 
                    'function': ClearFloor,
                    'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (x, y, 100)},
                    'on_success': [ActionBot.NEXT_ACTION],
                    'on_failed': []
                }

    return action_dict

def UpgradeDeamonTower(args):
    item_slot = args
    net.SendRefinePacket(item_slot, 4)
    return True

def GoBuyItemsFromNPC(args):
    items_slots_list_to_buy = args[0]
    npc_id = args[1]
    npc_position_x, npc_position_y = args[2]
    callback = args[3]

    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y)], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict

    npc = NPCAction(npc_id, event_answer=[1])
    NPCInteraction.RequestBusinessNPCClose(items_slots_list_to_buy, [], npc, callback)
    return True
    
def GetEnergyFromAlchemist(args):
    items_id_to_use = args[0]
    alchemist_id = args[1]
    npc_position_x, npc_position_y = args[2]
    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y), OpenLib.GetPlayerEmpireFirstMap()], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict
    

    for _id in items_id_to_use:
        item_slot = OpenLib.GetItemByID(_id)
        if item_slot < 0:
            continue
        alchemist_vid = OpenLib.GetInstanceByID(alchemist_id)
        if alchemist_vid != -1:
            action_dict = {'args': [alchemist_vid, item_slot], # position
                            'function': UsingItemOnInstance,
                            'requirements': {},
                            'on_success': [ActionBot.NEXT_ACTION],
                            'on_failed': [ActionBot.NEXT_ACTION],
                            }
            return action_dict

    
    return True

def ChangeEnergyToCrystal(args):
    alchemist_id = args[0]
    npc_position_x, npc_position_y = args[1]
    map_name = args[2]
    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y), 250], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)},
                        'on_success': [ActionBot.NEXT_ACTION],
                        }
        return action_dict
    energy_crystal = OpenLib.GetItemByID(51001)
    if player.GetItemCount(energy_crystal) >= 30:
        answer = [5,254,254,0,254]
        action_dict = { 'args': [alchemist_id, (npc_position_x, npc_position_y), answer, map_name], # ID, event_answer, posiiton of npc, npc's map
                          'function': TalkWithNPC,
                          'on_success': [ActionBot.NEXT_ACTION],
                          'requirements': {},

            }
        return action_dict
    return True

def TalkWithNPC(args):
    npc_id = args[0]
    npc_position_x, npc_position_y = args[1]
    event_answer = args[2]
    map_name = args[3]

    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y, 500):
        action_dict = {'args': [(npc_position_x, npc_position_y)], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict
    
    vid = OpenLib.GetInstanceByID(npc_id)
    if vid >= 0:
        net.SendOnClickPacket(vid)
        OpenLib.skipAnswers(event_answer, False)
        return True
    return False
    
def MineOre(args):
    selectedOre = args[0]
    is_curr_mining = args[1]()
    if eXLib.IsDead(selectedOre):
        return True
    

    can_mine = False
    idx = player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WEAPON)
    if idx != 0:
        item.SelectItem(idx)
        if item.GetItemType() == item.ITEM_TYPE_PICK:
            can_mine = True
    
    if not can_mine:
        pickaxe_slot = OpenLib.GetItemByID(29101)
        if pickaxe_slot > -1:
            chat.AppendChat(3, 'pickaxe slot '+str(pickaxe_slot))
            net.SendItemUsePacket(pickaxe_slot)   
        else:
            can_mine = False

    if not can_mine:
        idx = player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WEAPON)
        if idx != 0:
            item.SelectItem(idx)
            if item.GetItemType() == item.ITEM_TYPE_PICK:
                can_mine = True

    if not OpenLib.isPlayerCloseToInstance(selectedOre):
        action_dict = {'args': [selectedOre],
                        'function': MoveToVID,
                        'requirements': {ActionRequirementsCheckers.isNearInstance: [selectedOre]},
                        'on_success': [ActionBot.NEXT_ACTION]}
        return action_dict
                    
    if not is_curr_mining and can_mine:
        net.SendOnClickPacket(selectedOre)
        DebugPrint('Digging')
    
    return False
    
def LookForBlacksmithInDeamonTower(args):
    go_above_six_stage = args[0]
    item_index_to_upgrade = args[1]

    blacksmiths_id = [20074, 20075, 20076]

    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        for _id in blacksmiths_id:
            if chr.GetRace() == _id:
                if not OpenLib.isPlayerCloseToInstance(vid):
                    action_dict = {
                        'args': [vid],
                        'function': MoveToVID,
                        'requirements': { ActionRequirementsCheckers.IS_NEAR_INSTANCE: vid},
                        'on_failed': [ActionBot.NEXT_ACTION]
                    }

                    return action_dict

                if item_index_to_upgrade >= 0:
                    UpgradeDeamonTower(item_index_to_upgrade)
                
                if go_above_six_stage:
                    if player.GetStatus(player.LEVEL) < 75:
                        answer = [1, 1, 1]
                    else:
                        answer = [1, 1, 1, 1]
                
                else:
                    if player.GetStatus(player.LEVEL) < 75:
                        answer = [1, 1, 1]
                    else:
                        answer = [1, 1, 1, 254]
                    
                if answer:
                    blacksmith_x, blacksmith_y, blacksmith_z = chr.GetPixelPosition(vid)
                    action_dict = {
                        'args': [_id, (blacksmith_x, blacksmith_y), answer, 'metin2_map_deviltower1'],
                        'function': TalkWithNPC,
                        'on_success': [ActionBot.DISCARD],
                        'requirements': {},
                    }
                    return action_dict
                return True

            
    return False

def FindMapInDT(args):
    center_position = args[0]
    correct_map = OpenLib.GetItemByID(30302)
    unknow_old_chest = OpenLib.GetItemByID(30300)
    
    if correct_map >=0:
        net.SendItemUsePacket(player.EQUIPMENT, correct_map)
        return True

    if unknow_old_chest >=0:
        net.SendItemUsePacket(player.EQUIPMENT, unknow_old_chest)


    if not OpenLib.IsMonsterNearby():
        if OpenLib.isPlayerCloseToPosition(center_position[0], center_position[1], 300):
            return False
        else:
            action_dict = {'args': [(center_position[0], center_position[1]), 250], # position
                            'function': MoveToPosition,
                            'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (center_position[0], center_position[1])},
                            'on_success': [ActionBot.NEXT_ACTION],
                            }
            return action_dict

    action_dict = { 'args': [(center_position[0], center_position[1]), [_returnHasItemInterruptorWithArgs(30300), _returnHasItemInterruptorWithArgs(30302)]], # center position of area 
                'function': ClearFloor,
                'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (center_position[0], center_position[1])},
                'on_success': [ActionBot.NEXT_ACTION],
                'on_failed': []
            }

    return action_dict    

def OpenASealInMonument(args):
    center_position = args[0]
    correct_key = OpenLib.GetItemByID(30304)
    player_x, player_y, player_z = player.GetMainCharacterPosition()

    if not eXLib.FindPath(player_x, player_y, center_position[0], center_position[1]):
        return True

    if correct_key >=0:
        monument = OpenLib.getClosestInstance([OpenLib.OBJECT_TYPE])
        action_dict = {'args': [monument, correct_key], # position
                        'function': UsingItemOnInstance,
                        'requirements': {},
                        'on_success': [ActionBot.NEXT_ACTION],
                        'on_failed': [ActionBot.NEXT_ACTION],
                        }
        return action_dict
        
    
    action_dict = { 'args': [(center_position[0], center_position[1]), [_returnHasItemInterruptorWithArgs(30304)]], # center position of area 
                'function': ClearFloor,
                'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (center_position[0], center_position[1], 100)},
                'on_success': [ActionBot.NEXT_ACTION],
                'on_failed': []
            }

    return action_dict  

def ExchangeTrashItemsToEnergyFragments(args):
    from OpenBot.Modules import Settings
    first_map = OpenLib.GetPlayerEmpireFirstMap()
    OpenLog.DebugPrint(first_map)
    x, y = MapManager.GetNpcFromMap(first_map, 20001)
    return {'args': [Settings.instance.sellItems, 20001, (x, y)], # position
            'function': GetEnergyFromAlchemist,
            'requirements': {},
            'on_success': [ActionBot.DISCARD_PREVIOUS]
            }
    
def _returnHasItemInterruptorWithArgs(item_id):
    def x():
        if OpenLib.GetItemByID(item_id) > -1:
            return True
        return False
    return x
