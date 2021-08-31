from OpenBot.Modules.Skillbot.skillbot_module import instance


class SkillbotInterface:

    def GetStatus(self):
        return {
            'Enabled': instance.enabled,
            'TimeToWaitAfterLogout': instance.TimeToWaitAfterStart,
            'ShouldWaitAfterLogout': instance.shouldWait,
            'InstantMode': instance.instant_mode,
            'CurrentSkillSet': instance.currentSkillSet,
        }

    def Start(self):
        instance.Start()

    def Stop(self):
        instance.Stop()

    def SaveSettings(self, filename=''):
        if not type(filename) == str:
            return False
        instance.SaveSettings(filename)
        return True

    def LoadSettings(self, filename=''):
        if not type(filename) == str:
            return False
        instance.LoadSettings(filename)
        return True

    def SwitchSkill(self, skill_id):
        if not type(skill_id) == int:
            return False

        for skill in instance.CurrentSkillSet:
            if skill['id'] == skill_id:
                if skill['can_cast']:
                    skill['can_cast'] = False
                else:
                    skill['can_cast'] = True
                return True
        return False

    def SetCooldownForSkill(self, skill_id, cooldown):
        if not type(skill_id) == int or not type(cooldown) == int:
            return False
        for skill in instance.CurrentSkillSet:
            if skill['id'] == skill_id:
                skill['cooldown_time_instant_mode'] = cooldown
                return True
        return False

    def SwitchShouldWaitAfterLogout(self):
        if instance.shouldWait:
            instance.shouldWait = False
        else:
            instance.shouldWait = True

    def SwitchInstantMode(self):
        if instance.instant_mode:
            instance.instant_mode = False
        else:
            instance.instant_mode = True


interface = SkillbotInterface()

