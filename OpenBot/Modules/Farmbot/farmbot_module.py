from OpenBot.Modules.Actions import Action, ActionBot, ActionFunctions, ActionRequirementsCheckers
from OpenBot.Modules import OpenLog, OpenLib, FileManager,ChannelSwitcher
from OpenBot.Modules.OpenLog import DebugPrint
import player, ui, chat, chr, net, background
import eXLib

# STATES
WAITING_STATE = 0
WALKING_STATE = 1
MINING_STATE = 2
FARMING_STATE = 3
EXCHANGING_ITEMS_TO_ENERGY = 4

def OnDigMotionCallback(main_vid,target_ore,n):
    global farm
    if(main_vid != net.GetMainActorVID()):
        return
    if farm.enabled and farm.look_for_ore:
        DebugPrint('Digging is starting')
        farm.is_currently_digging = True
        slash_time = n * farm.MINING_SLASH_TIME
        ActionBot.instance.AddNewWaiter(slash_time, farm.IsCurrentlyDiggingDone)

def returnFuncWithArgs(func, args):
    def x():
        func(args)
    
    return x

class FarmingBot(ui.ScriptWindow):

    MINING_SLASH_TIME = 2.1

    def __init__(self):
        ui.Window.__init__(self)
        self.CURRENT_STATE = WALKING_STATE
        self.current_point = 0  # Current position index
        self.path = []  # list of tuples with coordinates [(0, 0, 'mapname'), (2, 2, 'map_name)] etc
        self.lastTime = 0
        self.enabled = False
        eXLib.RegisterDigMotionCallback(OnDigMotionCallback)
        self.slash_timer = OpenLib.GetTime()
        self.hasRecivedSlash = False
        self.lastTimeMine = 0   
        self.ores_vid_list = []
        self.ores_to_mine = []
        self.selectedOre = 0
        self.is_currently_digging = False
        self.metins_vid_list = []
        self.selectedMetin = 0
        self.isCurrActionDone = True
        self.lastTimeWaitingState = 0
        self.timeForWaitingState = 5
        self.isReadyToSwitchChannel = False
        

        self.switch_channels = False
        self.look_for_metins = False
        self.look_for_ore = False
        self.exchange_items_to_energy = False

    def __del__(self):
        ui.Window.__del__(self)

    def onStart(self):
        if len(self.path) > 1:
            self.enabled = True
            return True
        else:
            chat.AppendChat(3, 'You need add more than 1 waypoint!')
            self.enabled = False
            return False
    
    def onStop(self):
        self.enabled = False

    def IsWalkingDone(self):
        self.isCurrActionDone = True
        self.CURRENT_STATE = WALKING_STATE
        self.next_point()

    def IsDestroyingMetinDone(self):
        self.isCurrActionDone = True
        self.selectedMetin = 0
        self.CURRENT_STATE = WAITING_STATE
        self.lastTimeWaitingState = OpenLib.GetTime()

    def IsCurrentlyDiggingDone(self):
        self.is_currently_digging = False
        self.isCurrActionDone = True

    def IsExchangingItemsToEnergyFragmentsDone(self):
        self.isCurrActionDone = True
        self.CURRENT_STATE = WALKING_STATE

    def IsCurrentlyDigging(self):
        return self.is_currently_digging

    def load_path(self, filename):
        path = FileManager.FARMBOT_WAYPOINTS_LISTS + filename
        waypoints = FileManager.LoadListFile(path)
        self.path = []
        for point in waypoints:
            points = point.split(',')
            x = points[0][1:-1]
            y = points[1][1:-1]
            name = points[2][2:-2]
            self.path.append((float(x), float(y), str(name)))
        return True

    def save_path(self, filename):
        path = FileManager.FARMBOT_WAYPOINTS_LISTS + filename
        FileManager.SaveListFile(path, self.path)
        return True

    def add_point(self, point_dict):
        self.path.append((point_dict['x'], point_dict['y'], point_dict['map_name']))

    def delete_point(self, point_dict):
        for point in self.path:
            if point[0] == point_dict['x'] and point[1] == point_dict['y'] and point[2] == point_dict['map_name']:
                self.path.remove(point)
                return True
        return False

    def next_point(self):
        if self.current_point + 1 < len(self.path):
            self.current_point += 1
        else:
            self.path.reverse()
            self.current_point = 0
            if self.switch_channels:
                self.isReadyToSwitchChannel = True

    def select_metin(self):
        if self.metins_vid_list:
            self.selectedMetin = self.metins_vid_list.pop()

    def select_ore(self):
        if self.ores_vid_list:
            self.selectedOre = self.ores_vid_list.pop()

    def search_for_farm(self):
        if self.look_for_metins and len(self.metins_vid_list) > 0:
            self.select_metin()
            self.CURRENT_STATE = FARMING_STATE

        elif self.look_for_ore and len(self.ores_vid_list) > 0:
            self.select_ore()
            self.CURRENT_STATE = MINING_STATE
            return
        else:
            if not self.lastTimeWaitingState and not self.CURRENT_STATE == EXCHANGING_ITEMS_TO_ENERGY:
                self.CURRENT_STATE = WALKING_STATE

    def go_to_next_channel(self):
        action_dict = {
            'function_args': [ChannelSwitcher.GetNextChannel()],
            'function': ActionFunctions.ChangeChannel,
            'requirements': {ActionRequirementsCheckers.IS_IN_CHANNEL: [ChannelSwitcher.GetNextChannel()]},
            'on_success': [Action.NEXT_ACTION],
            'callback': self.SetIsCurrActionDoneTrue,
            #'call_only_once': True,
        }
        ActionBot.instance.AddNewAction(action_dict)

    def SetIsCurrActionDoneTrue(self):
        self.isCurrActionDone = True

    def checkForMetinsAndOres(self):
        self.ores_vid_list = []
        self.metins_vid_list = []
        for vid in eXLib.InstancesList:
            if OpenLib.IsThisOre(vid):
                chr.SelectInstance(vid)
                if chr.GetRace() in self.ores_to_mine:
                    self.ores_vid_list.append(vid)
            elif OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
                self.metins_vid_list.append(vid)

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
        if val and OpenLib.IsInGamePhase() and self.enabled:
            if self.isCurrActionDone:
                self.checkForMetinsAndOres()
                self.search_for_farm()

                if self.isReadyToSwitchChannel:
                    self.isReadyToSwitchChannel = False
                    self.isCurrActionDone = False
                    self.go_to_next_channel()
                    return

                if self.CURRENT_STATE == WAITING_STATE:

                    OpenLog.DebugPrint("[Farming-bot] WAITING_STATE")
                    text = self.edit_lineWaitingTime.GetText()
                    if self.is_text_validate(text):
                        self.timeForWaitingState = int(text)
                    val, self.lastTimeWaitingState = OpenLib.timeSleep(self.lastTimeWaitingState, self.timeForWaitingState)
                    if val:
                        self.lastTimeWaitingState = 0
                        self.CURRENT_STATE = WALKING_STATE
                    else:
                        self.search_for_farm()

                if self.CURRENT_STATE == WALKING_STATE:
                    OpenLog.DebugPrint("[Farming-bot] WALKING_STATE")
                    
                    if OpenLib.isInventoryFull():
                        from OpenBot.Modules import Settings
                        if self.exchange_items_to_energy:
                            for item in Settings.instance.sellItems:
                                slot=OpenLib.GetItemByID(item)
                                if slot > -1:
                                    OpenLog.DebugPrint('changing state to exchaning items')
                                    self.CURRENT_STATE = EXCHANGING_ITEMS_TO_ENERGY
                                    return
                    else:
                        OpenLog.DebugPrint('inventory is not full')
                    OpenLog.DebugPrint('No trash items')

                    interruptors_args = []
                    interruptors = []

                    if self.look_for_metins:
                        interruptors_args.append(0)
                        interruptors.append(ActionRequirementsCheckers.isMetinNearly)

                    if self.look_for_ore:
                        interruptors_args.append(self.ores_to_mine)
                        interruptors.append(ActionRequirementsCheckers.isRaceNearly)

                    if interruptors:
                        interrupt_function = lambda: Action.NEXT_ACTION
                    else:
                        interrupt_function = None

                    action_dict = {
                    'function_args': [(self.path[self.current_point][0], self.path[self.current_point][1]), self.path[self.current_point][2]],
                    'function': ActionFunctions.MoveToPosition, 
                    'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [self.path[self.current_point][0],
                                                                                self.path[self.current_point][1], 300],
                                                                                ActionRequirementsCheckers.IS_IN_MAP: [self.path[self.current_point][2]]},
                    'callback': self.IsWalkingDone,
                    'interruptors_args': interruptors_args,
                    'interruptors': interruptors,
                    'interrupt_function': interrupt_function}
                    ActionBot.instance.AddNewAction(action_dict)
                    self.isCurrActionDone = False
                    return

                elif self.CURRENT_STATE == MINING_STATE:
                    OpenLog.DebugPrint("[Farming-bot] MINING_STATE")
                    action_dict = {
                        'function_args': [self.selectedOre, self.IsCurrentlyDigging],
                        'requirements': {},
                        'function': ActionFunctions.MineOre,
                        'on_success': [Action.NEXT_ACTION],
                        'on_failed': [Action.NEXT_ACTION]
                    }

                    ActionBot.instance.AddNewAction(action_dict)
                    self.isCurrActionDone = False
                    return

                elif self.CURRENT_STATE == FARMING_STATE:
                    OpenLog.DebugPrint("[Farming-bot] FARMING_STATE")
                    action_dict = {'function_args': [0, self.selectedMetin],
                                'function': ActionFunctions.Destroy,
                                'requirements': {},
                                'on_success': [Action.NEXT_ACTION],
                                'on_failed': [],
                                'callback': self.IsDestroyingMetinDone
                                }
                    ActionBot.instance.AddNewAction(action_dict)
                    self.isCurrActionDone = False
                    return
                
                elif self.CURRENT_STATE == EXCHANGING_ITEMS_TO_ENERGY:
                    OpenLog.DebugPrint('[Farming-bot] EXCHANGING_STATE')
                    action_dict = {'function_args': [],
                                    'function': ActionFunctions.ExchangeTrashItemsToEnergyFragments,
                                    'on_success': [Action.NEXT_ACTION],
                                    'callback': self.IsExchangingItemsToEnergyFragmentsDone}
                    ActionBot.instance.AddNewAction(action_dict)
                    self.isCurrActionDone = False
                    return

farm = FarmingBot()
farm.Show()