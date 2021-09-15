from OpenBot.Modules.Actions.ActionBot import instance
from OpenBot.Modules.Actions import Action
from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import OpenLib


class ActionBotInterface:

    def SetStatus(self, status):
        if status['Enabled'] != instance.enabled: self.SwitchEnabled()
        if status['AlwaysUseWaithack'] != instance.showAlwaysWaithackButton: self.SwitchAlwaysUseWaithack()
        if status['DontUseWaithack'] != instance.showOffWaithackButton: self.SwitchDontUseWaithack()

        if 'ClearActions' in status.keys():
            self.ClearActions()
        if 'ClearWaiters' in status.keys():
            self.ClearWaiters()
        
            

    def GetStatus(self):
        return {
            'Enabled': instance.enabled,
            'Actions': self.GetActions(),
            'AlwaysUseWaithack': instance.showAlwaysWaithackButton,
            'DontUseWaithack': instance.showOffWaithackButton,
        }
    
    def GetActions(self):
        actions = []
        if instance.currActionObject == None:
            return actions
        actions.append({
            'name': instance.currActionObject.name
        })

        for action in instance.currActionsQueue:
            actions.append({
            'name': action.name
            })

        return actions  

    def SwitchEnabled(self):
        if instance.enabled:
            instance.enabled = False
        else:
            instance.enabled = True
    
    def SwitchAlwaysUseWaithack(self):
        if instance.showAlwaysWaithackButton:
            instance.showAlwaysWaithackButton = False
        else:
            instance.showAlwaysWaithackButton = True
        
    def SwitchDontUseWaithack(self):
        if instance.showOffWaithackButton:
            instance.showOffWaithackButton = False
        else:
            instance.showOffWaithackButton = True

    def AddAction(self, action):
        if type(action) == Action.Action:
            instance.currActionsQueue.append(action)
        else:
            new_action = instance.ConvertDictActionToObjectAction(action)
            DebugPrint('Converted Dict action to object action')
            instance.currActionsQueue.append(new_action)   

    def AddWaiter(self, timeToWait, callback):
        instance.waiters.append({
            'timeToWait': timeToWait,
            'callback': callback,
            'launching_time': OpenLib.GetTime(),
        })  

    def ClearActions(self):
        if instance.currActionObject is not None:
            instance.currActionObject.CallCallback()

        for action in instance.currActionsQueue:
            action.CallCallback()
        
        self.currActionObject = None
        self.currActionsQueue = []
    
    def ClearWaiters(self):
        for waiter in instance.waiters:
            waiter['callback']()
        
        instance.waiters = []

action_bot_interface = ActionBotInterface()