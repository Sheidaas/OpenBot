import ActionRequirementsCheckers 
from BotBase import BotBase
from OpenLog import DebugPrint

# ON_SUCCESS FLAGS
NEXT_ACTION = 'next_action'

# ON ACTION RETURN FLAGS
DISCARD = 'discard'

# STATES
STATE_CANCELING = -1
STATE_STOP = 0


class ActionBot(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.2)
        self.currState = STATE_STOP

        self.currActionDict = None
        self.currActionsDictsQueue = []

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

    def GoToNextAction(self, skipRequirements=False):
        if skipRequirements:
            if 'callback' in self.currActionDict.keys():
                self.currActionDict['callback']()
            if self.currActionsDictsQueue:
                self.currActionDict = self.currActionsDictsQueue.pop()
            else:
                self.currActionDict = None
        else:
            if self.CheckRequirementsForCurrAction:
                if 'callback' in self.currActionDict.keys():
                    self.currActionDict['callback']()
                if self.currActionsDictsQueue:
                    self.currActionDict = self.currActionsDictsQueue.pop()
                else:
                    self.currActionDict = None
        DebugPrint(str(self.currActionDict['function']) + ' SUCCESS ADD ACTION')

    def DoAction(self, action_dict):
        args = action_dict['args']
        action = action_dict['function']
        return action(args)

    def NewActionReturned(self, action_dict):
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


    def Frame(self):
        if self.currActionDict == None:
            if not self.CheckIsThereNewAction():
                return

        is_action_done = self.DoAction(self.currActionDict)

        if type(is_action_done) == bool:

            if 'on_success' in self.currActionDict.keys() and is_action_done:
                #DebugPrint(str(action_dict['function']) + ' SUCCESS_CASE')
                if NEXT_ACTION in self.currActionDict['on_success']:
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

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

instance = ActionBot()
