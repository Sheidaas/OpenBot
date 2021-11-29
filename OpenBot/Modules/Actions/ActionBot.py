from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
import Action
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import OpenLib
from OpenBot.Modules import Hooks
import ui, chat

STATES = {
    'WAITING': 'waiting',
    'RUNNING': 'running'
}


def _afterLoadPhase(phase, phaseWnd):
    global instance
    if OpenLib.IsInGamePhase():
        for waiter in instance.waiters:
            waiter['callback']()
        instance.waiters = []

        instance.currentState = STATES['WAITING']


class ActionBot(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.currentState = STATES['WAITING']
        self.lastTime = 0
        self.enabled = True
        self.currActionObject = None
        self.currActionsQueue = []

        self.waiters = []


        self.showOffWaithackButton = False
        self.showAlwaysWaithackButton = False

    def GetNewId(self):
        used_id = []
        if self.currActionObject is not None:
            used_id.append(self.currActionObject.id)
        [used_id.append(action.id) for action in self.currActionsQueue]
        for new_id in range(len(self.currActionsQueue)+2):
            if new_id not in used_id:
                return new_id
        return -1

    def DiscardActionByParent(self, parent):
        if parent is True:
            return True

        if self.currActionObject is not None:
            if self.currActionObject.parent == parent:
                new_parent = self.currActionObject.id
                self.currActionObject = None
                return self.DiscardActionByParent(new_parent)

        for action in self.currActionsQueue:
            if action.parent == parent:
                new_parent = action.id
                self.currActionsQueue.remove(action)
                return self.DiscardActionByParent(new_parent)

        return True

    def GoToNextAction(self):
        if self.currActionObject.callback is not None:
            DebugPrint('Calling callback')
            self.currActionObject.CallCallback()

        if self.currActionsQueue:
            self.currActionObject = self.currActionsQueue.pop()
        else:
            self.currActionObject = None

    def ConvertDictActionToObjectAction(self, action_dict):
        action_dict_keys = action_dict.keys()
        if 'function' not in action_dict_keys and 'function_args' not in action_dict_keys:
            DebugPrint('Action dict dont have function or function_args!')
            return
        new_action = Action.Action(_id=self.GetNewId,
                            function=action_dict['function'])

        for key in action_dict_keys:
            if key is not 'function':
                setattr(new_action, key, action_dict[key])
        
        return new_action
        
    def NewActionReturned(self, action):
        if not self.currActionObject in self.currActionsQueue and self.currActionObject is not None:
            self.currActionsQueue.append(self.currActionObject)

        if isinstance(action, Action.Action):
            self.currActionObject = action
        else:
            new_action = self.ConvertDictActionToObjectAction(action)
            DebugPrint(str(action))
            self.currActionObject = new_action

    def CheckIsThereNewAction(self):
        if not len(self.currActionsQueue):
            return False
        else:
            self.currActionObject = self.currActionsQueue.pop()
            return True   

    def FrameDoAction(self):
        action_result = self.currActionObject.CallFunction()
        #DebugPrint(str(self.currActionsQueue))
        #DebugPrint(str(action_result))
        if type(action_result) == str:
            
            if action_result == Action.NEXT_ACTION:
                self.GoToNextAction()
                DebugPrint('Action do NEXT_ACTION')

            elif action_result == Action.DISCARD_PREVIOUS:
                self.GoToNextAction()
                self.GoToNextAction()
                DebugPrint('Action do DISCARD_PREVIOUS')
            
            elif action_result == Action.REQUIREMENTS_NOT_DONE:
                DebugPrint('Action do REQUIREMENTS_NOT_DONE')

            elif action_result == Action.NOTHING:
                DebugPrint('Action do nothing')
                
            elif action_result == Action.ERROR:
                DebugPrint('Action has some error')
                self.GoToNextAction()
        
        elif isinstance(action_result, Action.Action) or type(action_result) == dict:
            DebugPrint('New action returned')
            action_result['parent'] = self.currActionObject.id
            self.NewActionReturned(action_result)

    def OnUpdate(self):
        if self.currentState == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 2)
            if val:
                self.currentState = STATES['RUNNING']

        if self.currentState == STATES['RUNNING']:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
            if val and OpenLib.IsInGamePhase() and self.enabled:
                self.rendered_actions = []
                self.rendered_waiters = []
                names = ['Going to enemy']

                this_time = OpenLib.GetTime()
                for waiter in self.waiters:
                    if this_time >= waiter['timeToWait'] + waiter['launching_time']:
                        waiter['callback']()
                        self.waiters.remove(waiter)

                if self.currActionObject == None:
                    if not self.CheckIsThereNewAction():
                        return

                if not self.showOffWaithackButton:
                    if self.showAlwaysWaithackButton:
                        waithack_interface.Start()
                    else:
                        if self.currActionObject.function.__name__ in ['DestroyByID', 'DestroyByVID', 'ClearFloor', 'LookForBlacksmithInDeamonTower',
                                                                    'FindMapInDT', 'OpenASealInMonument'] or \
                            self.currActionObject.name in names:
                            waithack_interface.Start()
                        else:
                            waithack_interface.Stop()
                else:
                    waithack_interface.Start()

                self.FrameDoAction()

instance = ActionBot()
instance.Show()
Hooks.registerPhaseCallback('actionBot', _afterLoadPhase)
