from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
import Action, ActionFunctions
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import OpenLib
from OpenBot.Modules import Hooks, Movement
import ui, chat, player

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

        self.last_position = []
        self.attempts = 0
        self.was_position_saved = False

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
        #player.SetAttackKeyState(False)
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

    def GoToNextAction(self, discard=False):
        if not discard:
            if self.currActionObject.callback is not None:
                DebugPrint('Calling callback')
                self.currActionObject.CallCallback()
        else:
            if self.currActionObject.callback_on_failed is not None:
                DebugPrint(self.currActionObject.name)
                DebugPrint('Calling callback_on_falied')
                self.currActionObject.callback_on_failed()

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
            self.currActionObject = new_action

    def CheckIsThereNewAction(self):
        if not len(self.currActionsQueue):
            return False
        else:
            self.currActionObject = self.currActionsQueue.pop()
            return True   

    def FrameDoAction(self):
        action_result = self.currActionObject.CallFunction()
        if type(action_result) == str:
            
            if action_result == Action.NEXT_ACTION:
                self.GoToNextAction()
                DebugPrint('Action do NEXT_ACTION')

            elif action_result == Action.DISCARD:
                self.GoToNextAction(discard=True)
                DebugPrint('Action do DISCARD')
            
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

        if self.currActionObject is not None:
            if not self.currActionObject.function == ActionFunctions.MoveToPosition:
                return
            x, y, z = player.GetMainCharacterPosition()
            if self.was_position_saved:
                if self.last_position == [x, y]:
                    self.attempts += 1
                if self.attempts > 100:
                    self.DiscardActionByParent(self.currActionObject.parent)
                    self.was_position_saved = False
                    self.last_position = []
                    self.attempts = 0
            else:
                self.was_position_saved = True
                self.last_position = [x, y]


    def should_run_waithack(self):
        from OpenBot.Modules.Protector.protector_module import protector_module
        names = ['Going to enemy', 'DestroyByID', 'DestroyByVID',
                 'ClearFloor', 'LookForBlacksmithInDeamonTower',
                 'FindMapInDT', 'OpenASealInMonument']

        if protector_module.avoid_players and protector_module.is_unknown_player_close:
            return False

        if self.showOffWaithackButton:
            return False

        if self.currActionObject.function.__name__ in names or self.currActionObject.name in names:
            return True

        if self.showAlwaysWaithackButton:
            return True

    def OnUpdate(self):
        if self.currentState == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 2)
            if val:
                self.currentState = STATES['RUNNING']

        if self.currentState == STATES['RUNNING']:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
            if val and OpenLib.IsInGamePhase() and self.enabled:


                this_time = OpenLib.GetTime()
                for waiter in self.waiters:
                    if this_time >= waiter['timeToWait'] + waiter['launching_time']:
                        waiter['callback']()
                        self.waiters.remove(waiter)

                if self.currActionObject is None:
                    if not self.CheckIsThereNewAction():
                        waithack_interface.Stop()
                        return

                if self.should_run_waithack():
                    waithack_interface.Start()
                else:
                    waithack_interface.Stop()

                self.FrameDoAction()

instance = ActionBot()
instance.Show()
Hooks.registerPhaseCallback('actionBot', _afterLoadPhase)
