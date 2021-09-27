from OpenBot.Modules.Schema.schema_runner_module import instance

class SchemaRunnerInterface:

    def SetStatus(self, status):
        pass

    def GetStatus(self):
        pass

    def SetNewSchema(self, schema):
        instance.currStage = 0
        instance.currAction = 0
        instance.isCurrActionDone = True
        instance.currSchema = schema
    
    def DiscardCurrentSchema(self):
        instance.currStage = 0
        instance.currAction = 0
        instance.isCurrActionDone = True
        instance.currSchema = None

    def SwitchEnabled(self):
        if instance.enabled:
            instance.enabled = False
        else:
            instance.enabled = True
        instance.currStage = 0
        instance.currAction = 0
        instance.isCurrActionDone = True

schema_runner_interface = SchemaRunnerInterface()