from OpenBot.Modules.Schema.schema_runner_module import instance

class SchemaRunnerInterface:

    def SetStatus(self, status):
        if status['Enabled'] != instance.enabled:
            self.SwitchEnabled()
        status_keys = status.keys()
        if 'ResetSchema' in status_keys:
            self.ResetSchema()

    def GetStatus(self):
        return {
            'Enabled': instance.enabled,
            'CurrSchema': str(instance.currSchema),
            'CurrStage': instance.currStage,
            'CurrAction': instance.currAction,
            'CurrRepeat': instance.currRepeat
        }
        
    def ResetSchema(self):
        instance.currStage = 0
        instance.currAction = 0
        instance.isCurrActionDone = True
        instance.currRepeat = 0

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