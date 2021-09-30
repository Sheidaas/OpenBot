from OpenBot.Modules import OpenLib, OpenLog
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
import ui


class SchemaRunnerModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.enabled = True
        self.currSchema = None
        self.currStage = 0
        self.currAction = 0
        self.isCurrActionDone = True

        self.currRepeat = 0
        self.lastTime = 0

    def DiscardCurrentSchema(self):
        self.currSchema = None
        self.currStage = 0
        self.currAction = 0
        self.isCurrActionDone = True
        self.currRepeat = 0

    def SetIsCurrActionDoneTrue(self):
        self.GoToNextAction()
        self.isCurrActionDone = True

    def GoToNextAction(self):
        if self.currSchema != None:
            if self.currAction + 1 < len(self.currSchema.stages[str(self.currStage)]['ACTIONS']):
                self.currAction += 1
            else:
                OpenLog.DebugPrint('Stage Complete')
                self.GoToNextStage()

    def GoToNextStage(self):
        self.currAction = 0
        if self.currStage + 1 < len(self.currSchema.stages.keys()):
            self.currStage += 1
        else:
            if self.currRepeat + 1 < self.currSchema.options['Repeats']:
                self.currRepeat += 1
                self.currStage = 0
                self.currAction = 0
                OpenLog.DebugPrint(str(self.currRepeat) + '/' + str(self.currSchema.options['Repeats']))
                return
            OpenLog.DebugPrint('Schema Complete')
            self.currSchema = None
            self.isCurrActionDone = True
            self.currStage = 0
            self.currAction = 0
            self.currRepeat = 0

    def GetCurrentAction(self):
        return self.currSchema.stages[str(self.currStage)]['ACTIONS'][self.currAction]

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
        if val and OpenLib.IsInGamePhase() and self.enabled and self.isCurrActionDone and self.currSchema != None:
            action = self.GetCurrentAction()
            OpenLog.DebugPrint(str(action['name']) + ' is currently running')
            if action['function'].__name__ == 'BuyItemsForAlchemist':
                action['function_args'].append(self.SetIsCurrActionDoneTrue)
                action_bot_interface.AddAction(action)
                self.isCurrActionDone = False
                return
            action['callback'] = self.SetIsCurrActionDoneTrue
            action_bot_interface.AddAction(action)
            self.isCurrActionDone = False

instance = SchemaRunnerModule()
instance.Show()