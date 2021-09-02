from OpenBot.Modules.OpenLog import DebugPrint
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
        instance.onStart()
        DebugPrint('Skillbot started' + str(instance.enabled))

    def Stop(self):
        instance.onStop()
        DebugPrint('Skillbot stopped' + str(instance.enabled))

    def SaveSettings(self, filename=''):
        if not type(filename) == str:
            return False
        instance.SaveSettings(filename)
        DebugPrint('Skillbot save settings to ' + str(filename))
        return True

    def LoadSettings(self, filename=''):
        if not type(filename) == str:
            return False
        instance.LoadSettings(filename)
        DebugPrint('Skillbot load settings from ' + str(filename))
        return True

    def ResetSkills(self):
        instance.resetSkills()
        DebugPrint('Skillbot reset skills')
    
    def SetCooldownForSkill(self, skill_id, cooldown):
        #DebugPrint(str(skill_id))
        for skill in instance.currentSkillSet:
            if skill['id'] == skill_id:
                if skill['cooldown_time_instant_mode'] == cooldown:
                    return True
                skill['cooldown_time_instant_mode'] = cooldown
                DebugPrint('skill ' + str(skill_id) + ' cooldown set to ' + str(cooldown))
                return True
        return False

    def SetTimeToWaitAfterLogout(self, time):
        instance.TimeToWaitAfterStart = time

    def SwitchSkill(self, skill_id):
        if not type(skill_id) == int:
            return False

        for skill in instance.currentSkillSet:
            if skill['id'] == skill_id:
                if skill['can_cast']:
                    skill['can_cast'] = False
                else:
                    skill['can_cast'] = True
                DebugPrint(str(skill) + ' was updated')
                return True
        DebugPrint('There is no skill with id ' + str(skill_id))
        return False

    def SwitchStartUpWait(self):
        if instance.startUpWait:
            instance.startUpWait = False
        else:
            instance.startUpWait = True
        DebugPrint('Skillbot switch startupwait')

    def SwitchShouldWaitAfterLogout(self, val=None):
        if instance.shouldWait:
            instance.shouldWait = False
        else:
            instance.shouldWait = True
        DebugPrint('Skillbot switch startupwait')


    def SwitchInstantMode(self, val=None):
        if instance.instant_mode:
            instance.instant_mode = False
        else:
            instance.instant_mode = True
        DebugPrint('Skillbot switch instant_mode')


interface = SkillbotInterface()

