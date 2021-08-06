from OpenBot.Modules import DmgHacks
import ActionRequirementsCheckers
from OpenBot.Modules.BotBase import BotBase
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import OpenLib, UIComponents
from OpenBot.Modules import Hooks
import ui, chat


# ON_SUCCESS FLAGS
NEXT_ACTION = 'next_action'

# ON ACTION RETURN FLAGS
DISCARD = 'discard'
DISCARD_PREVIOUS = 'discard_previous'

# STATES
STATE_CANCELING = -1
STATE_STOP = 0

# STAGES OPTIONS
STAGE_REPEAT = 'stage_reapat'

def _afterLoadPhase(phase):
    global instance
    if phase == OpenLib.PHASE_LOGIN or OpenLib.PHASE_GAME:
        instance.enableActionBot.SetOn()
        instance.Start()
        for waiter in instance.waiters:
            waiter['callback']()
        instance.waiters = []


class ActionBot(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.2)

        self.currState = STATE_STOP

        self.currActionDict = None
        self.currActionsDictsQueue = []

        self.waiters = []

        self.BuildWindow()

    def BuildWindow(self):
        self.comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 275)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('ActionBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = UIComponents.Component()

        self.TabWidget = UIComponents.TabWindow(10, 30, 215, 235, self.Board, ['General', 'Settings'])

        self.general = self.TabWidget.GetTab(0)
        self.settings_tab = self.TabWidget.GetTab(1)

        self.enableActionBot = comp.OnOffButton(self.general, '', '', 170, 135,
                                                    OffUpVisual='OpenBot/Images/start_0.tga',
                                                    OffOverVisual='OpenBot/Images/start_1.tga',
                                                    OffDownVisual='OpenBot/Images/start_2.tga',
                                                    OnUpVisual='OpenBot/Images/stop_0.tga',
                                                    OnOverVisual='OpenBot/Images/stop_1.tga',
                                                    OnDownVisual='OpenBot/Images/stop_2.tga',
                                                    funcState=self.OnEnableSwitchButton, defaultValue=False)
        
        self.ClearButton = comp.Button(self.general, 'Clear', '', 20, 135, self.OnClearButton,
                                          'd:/ymir work/ui/public/large_Button_01.sub',
                                          'd:/ymir work/ui/public/large_Button_02.sub',
                                          'd:/ymir work/ui/public/large_Button_03.sub')
        self.ShowButton = comp.Button(self.general, 'Show', '', 20, 155, self.OnClearButton,
                                          'd:/ymir work/ui/public/large_Button_01.sub',
                                          'd:/ymir work/ui/public/large_Button_02.sub',
                                          'd:/ymir work/ui/public/large_Button_03.sub')
        
        self.showAlwaysWaithackButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tAlways use waithack', 'If check, waithack will be turned on even while walking', 20, 20,
                                                         funcState=self.switch_always_use_waithack,
                                                         defaultValue=False)

        self.showOffWaithackButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tDont use waithack', 'If checked, farmbot wont use waithack for destroying metin', 20, 40,
                                                      funcState=self.switch_dont_use_waithack,
                                                      defaultValue=False)

    def switch_always_use_waithack(self, val):
        if val:
            self.showOffWaithackButton.SetOff()

    def switch_dont_use_waithack(self, val):
        if val:
            self.showAlwaysWaithackButton.SetOff()

    def CheckRequirementsForCurrAction(self):
        requirements = self.currActionDict['requirements']

        for requirement in requirements:

            if requirement == ActionRequirementsCheckers.IS_IN_MAP:
                if not ActionRequirementsCheckers.isInMaps(requirements[requirement]):
                    return False
            
            elif requirement == ActionRequirementsCheckers.IS_ON_POSITION:
                if not ActionRequirementsCheckers.isOnPosition(requirements[requirement]):
                    return False
            
            elif requirement == ActionRequirementsCheckers.IS_NEAR_POSITION:
                if not ActionRequirementsCheckers.isNearPosition(requirements[requirement]):
                    return False
            
            elif requirement == ActionRequirementsCheckers.IS_NEAR_INSTANCE:
                if not ActionRequirementsCheckers.isNearInstance(requirements[requirement]):
                    return False


        return True

    def OnEnableSwitchButton(self, val):
        if val:
            self.Start()
        else:
            self.Stop()
            
    def OnClearButton(self):
        self.currActionDict = None
        self.currActionsDictsQueue = []
        for waiter in self.waiters:
            waiter['callback']()
        self.waiters = []

    def GoToNextAction(self, skipRequirements=False):
        if skipRequirements:
            if 'callback' in self.currActionDict.keys():
                DebugPrint('Calling callback')
                self.currActionDict['callback']()
            if self.currActionsDictsQueue:
                self.currActionDict = self.currActionsDictsQueue.pop()
            else:
                self.currActionDict = None
        else:
            DebugPrint('checking req')
            if self.CheckRequirementsForCurrAction():
                if 'callback' in self.currActionDict.keys():
                    DebugPrint('Calling callback')
                    self.currActionDict['callback']()
                if self.currActionsDictsQueue:
                    self.currActionDict = self.currActionsDictsQueue.pop()
                else:
                    self.currActionDict = None

    def DoAction(self, action_dict):
        args = action_dict['args']
        action = action_dict['function']
        return action(args)

    def NewActionReturned(self, action_dict):
        if not self.currActionDict in self.currActionsDictsQueue:
            self.currActionsDictsQueue.append(self.currActionDict)
        self.currActionDict = action_dict

    def AddNewAction(self, action_dict):
        self.currActionsDictsQueue.append(action_dict)

    def CheckIsThereNewAction(self):
        if not len(self.currActionsDictsQueue):
            return False
        else:
            self.currActionDict = self.currActionsDictsQueue.pop()
            return True

    def StopBot(self):
        self.OnClearButton()

    def Frame(self):
        self.rendered_actions = []
        self.rendered_waiters = []

        if self.Board.IsShow():
            self.RefreshRenderedWaiters()

        for waiter in self.waiters:
            this_time = OpenLib.GetTime()
            if this_time > waiter['timeToWait'] + waiter['launching_time']:
                waiter['callback']()
                self.waiters.remove(waiter)
        if self.currActionDict == None:
            if not self.CheckIsThereNewAction():
                return

        if not self.showOffWaithackButton.isOn:
            if self.showAlwaysWaithackButton.isOn:
                DmgHacks.Resume()
            else:
                if self.currActionDict['function'].__name__ in ['Destroy', 'ClearFloor', 'LookForBlacksmithInDeamonTower',
                                                               'FindMapInDT', 'OpenASealInMonument']:
                    DmgHacks.Resume()
                else:
                    DmgHacks.Pause()
        else:
            DmgHacks.Pause()
        
        self.FrameDoAction()

    def AddNewWaiter(self, timeToWait, callback):
        self.waiters.append({
            'timeToWait': timeToWait,
            'callback': callback,
            'launching_time': OpenLib.GetTime(),
        })     

    def FrameDoAction(self):
        if self.Board.IsShow():
            self.RefreshRenderedActions()
        is_action_done = self.DoAction(self.currActionDict)
        if type(is_action_done) == bool:

            if 'on_success' in self.currActionDict.keys() and is_action_done:
                
                for key in self.currActionDict['on_success']:
                    if callable(key):
                        if key():
                            self.GoToNextAction()
                    elif type(key) == str:
                        if key == NEXT_ACTION:
                            self.GoToNextAction()
                        elif key == DISCARD_PREVIOUS:
                            previous = self.currActionsDictsQueue.pop()
                            if 'callback' in previous.keys():
                                previous['callback']()
                            self.GoToNextAction()


            elif 'on_failed' in self.currActionDict.keys() and not is_action_done:
                
                for key in self.currActionDict['on_failed']:
                    if callable(key):
                        if key():
                            self.GoToNextAction(skipRequirements=True)
                    elif type(key) == str:
                        if key == NEXT_ACTION:
                            self.GoToNextAction(skipRequirements=True)
                
            
            else:
                #DebugPrint(str(action_dict['function']) + ' CHECKING REQ')
                self.GoToNextAction()

        else:
            self.NewActionReturned(is_action_done)

    def RefreshRenderedActions(self):
        actions_to_render = [self.currActionDict] + self.currActionsDictsQueue[:5]
        self.rendered_actions = []
        x = 10
        y = 15
        comp = UIComponents.Component()
        for action in actions_to_render:
            self.rendered_actions.append(comp.TextLine(self.general, action['function'].__name__, x, y, UIComponents.RGB(255, 255, 255)))
            y += 20
    
    def RefreshRenderedWaiters(self):
        x = 100
        y = 15
        self.rendered_waiters = []
        comp = UIComponents.Component()
        for action in self.waiters:
            self.rendered_waiters.append(comp.TextLine(self.general, action['callback'].__name__, x, y, UIComponents.RGB(255, 255, 255)))
            y += 20

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

instance = ActionBot()
Hooks.registerPhaseCallback('actionBot', _afterLoadPhase)
