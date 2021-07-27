import ActionRequirementsCheckers 
from OpenBot.Modules.BotBase import BotBase
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import UIComponents
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

class ActionBot(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.2)
        self.currState = STATE_STOP

        self.currActionDict = None
        self.currActionsDictsQueue = []
        self.BuildWindow()

    def BuildWindow(self):
        self.comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 235)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('ActionBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = UIComponents.Component()
                                
        self.enableDeamonTower = comp.OnOffButton(self.Board, '', '', 150, 110,
                                                    OffUpVisual='OpenBot/Images/start_0.tga',
                                                    OffOverVisual='OpenBot/Images/start_1.tga',
                                                    OffDownVisual='OpenBot/Images/start_2.tga',
                                                    OnUpVisual='OpenBot/Images/stop_0.tga',
                                                    OnOverVisual='OpenBot/Images/stop_1.tga',
                                                    OnDownVisual='OpenBot/Images/stop_2.tga',
                                                    funcState=self.OnEnableSwitchButton, defaultValue=False)
        
        self.ClearButton = comp.Button(self.Board, 'Clear', '', 20, 110, self.OnClearButton,
                                          'd:/ymir work/ui/public/large_Button_01.sub',
                                          'd:/ymir work/ui/public/large_Button_02.sub',
                                          'd:/ymir work/ui/public/large_Button_03.sub')
        self.ShowButton = comp.Button(self.Board, 'Show', '', 20, 130, self.OnClearButton,
                                          'd:/ymir work/ui/public/large_Button_01.sub',
                                          'd:/ymir work/ui/public/large_Button_02.sub',
                                          'd:/ymir work/ui/public/large_Button_03.sub')

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

        return True

    def OnEnableSwitchButton(self, val):
        if val:
            self.Start()
        else:
            self.Stop()

    def OnShowButton(self):
        chat.AppendChat(3, str(self.currActionDict) + ' CURR ACTION DICT')
        chat.AppendChat(3, str(self.currActionsDictsQueue) + ' CURR ACTION DICT Queue')

    def OnClearButton(self):
        self.currActionDict = None
        self.currActionsDictsQueue = []

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
        if self.currActionDict == None:
            if not self.CheckIsThereNewAction():
                return

        self.RefreshRenderedActions()
        is_action_done = self.DoAction(self.currActionDict)
        DebugPrint(str(is_action_done))
        if type(is_action_done) == bool:

            if 'on_success' in self.currActionDict.keys() and is_action_done:
                #DebugPrint(str(action_dict['function']) + ' SUCCESS_CASE')
                if NEXT_ACTION in self.currActionDict['on_success']:
                    self.GoToNextAction()
                
                elif DISCARD_PREVIOUS in self.currActionDict['on_success']:
                    previous = self.currActionsDictsQueue.pop()
                    if 'callback' in previous.keys():
                        previous['callback']()
                    self.GoToNextAction()

            elif 'on_failed' in self.currActionDict.keys() and not is_action_done:
                #DebugPrint(str(action_dict['function']) + ' FAILED_CASE')
                if NEXT_ACTION in self.currActionDict['on_failed']:
                    self.GoToNextAction(skipRequirements=True)
            
            else:
                #DebugPrint(str(action_dict['function']) + ' CHECKING REQ')
                self.GoToNextAction()

        else:
            self.NewActionReturned(is_action_done)

    def RefreshRenderedActions(self):
        actions_to_render = [self.currActionDict] + self.currActionsDictsQueue
        x = 10
        y = 30
        comp = UIComponents.Component()
        for action in actions_to_render:
            text = comp.TextLine(self.Board, action['function'].__name__, x, y, UIComponents.RGB(255, 255, 255))
            setattr(self, 'rendered_action_x_' + str(y), text)
            y += 20

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

instance = ActionBot()
instance.switch_state()