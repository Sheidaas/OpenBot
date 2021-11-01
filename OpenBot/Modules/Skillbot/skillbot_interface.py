from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Skillbot.skillbot_module import instance

STATUS = {
    'ENABLED': 'Enabled',
    'TIME_TO_WAIT_AFTER_LOGOUT': 'TimeToWaitAfterLogout',
    'SHOULD_WAIT_AFTER_LOGOUT': 'ShouldWaitAfterLogout',
    'INSTANT_MODE': 'InstantMode',
    'CURRENT_SKILL_SET': 'CurrentSkillSet',
    'UPGRADE_SKILLS': 'UpgradeSkills',
    'UPGRADE_STATES': 'UpgradeStats',
    'FOLLOW_VID': 'FollowVID',
    'FOLLOWED_VID': 'FollowedVID',
    'UNMOUNT_HORSE': 'UnmountHorse',
    'STAT_TO_UPGRADE_ORDER': 'StatToUpgradeOrder'
}

class SkillbotInterface:

    def SetStatus(self, status):
        if status['Enabled']:
            self.Start()
        else:
            self.Stop()

        if status[STATUS['TIME_TO_WAIT_AFTER_LOGOUT']] != instance.TimeToWaitAfterStart:
            self.SetTimeToWaitAfterLogout(status[STATUS['TIME_TO_WAIT_AFTER_LOGOUT']])
        if status[STATUS['SHOULD_WAIT_AFTER_LOGOUT']] != instance.shouldWait:
            self.SwitchShouldWaitAfterLogout()
        if status[STATUS['INSTANT_MODE']] != instance.instant_mode:
            self.SwitchInstantMode()
        if status[STATUS['UPGRADE_SKILLS']] != instance.upgrade_skills:
            self.SwitchUpgradeSkills()
        if status[STATUS['UPGRADE_STATES']] != instance.upgrade_stats:
            self.SwitchUpgradeStats()
        if status[STATUS['FOLLOW_VID']] != instance.following_vid:
            self.SwitchFollowVID()
        if status[STATUS['FOLLOWED_VID']] != instance.followed_vid:
            instance.followed_vid = status[STATUS['FOLLOWED_VID']]
        if status[STATUS['UNMOUNT_HORSE']] != instance.unmount_horse:
            instance.unmount_horse = status[STATUS['UNMOUNT_HORSE']]
        if status[STATUS['STAT_TO_UPGRADE_ORDER']] != instance.stat_to_upgrade_order:
            instance.stat_to_upgrade_order = status[STATUS['STAT_TO_UPGRADE_ORDER']]


        for skill in range(len(status['CurrentSkillSet'])):
            if status['CurrentSkillSet'][skill]['can_cast'] != instance.currentSkillSet[skill]['can_cast']:
                self.SwitchSkill(status['CurrentSkillSet'][skill]['id'])
            if status['CurrentSkillSet'][skill]['cooldown_time_instant_mode'] != instance.currentSkillSet[skill]['cooldown_time_instant_mode']:
                self.SetCooldownForSkill(status['CurrentSkillSet'][skill]['id'], status['CurrentSkillSet'][skill]['cooldown_time_instant_mode'])
            if status['CurrentSkillSet'][skill]['upgrade_order'] != instance.currentSkillSet[skill]['upgrade_order']:
                self.SetUpgradeOrder(status['CurrentSkillSet'][skill]['id'], status['CurrentSkillSet'][skill]['upgrade_order'])

        instance.SaveSettings()

    def GetStatus(self):
        return {
            STATUS['ENABLED']: instance.enabled,
            STATUS['TIME_TO_WAIT_AFTER_LOGOUT']: instance.TimeToWaitAfterStart,
            STATUS['SHOULD_WAIT_AFTER_LOGOUT']: instance.shouldWait,
            STATUS['INSTANT_MODE']: instance.instant_mode,
            STATUS['CURRENT_SKILL_SET']: instance.currentSkillSet,
            STATUS['UPGRADE_SKILLS']: instance.upgrade_skills,
            STATUS['UPGRADE_STATES']: instance.upgrade_stats,
            STATUS['FOLLOW_VID']: instance.following_vid,
            STATUS['FOLLOWED_VID']: instance.followed_vid,
            STATUS['UNMOUNT_HORSE']: instance.unmount_horse,
            STATUS['STAT_TO_UPGRADE_ORDER']: instance.stat_to_upgrade_order
        }

    def Start(self):
        instance.onStart()

    def Stop(self):
        instance.onStop()

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

    def ResetSkills(self):
        instance.resetSkills()
    
    def SetCooldownForSkill(self, skill_id, cooldown):
        skill_to_change = [skill for skill in instance.currentSkillSet if skill['id'] == skill_id]
        if not skill_to_change:
            return False
        skill_to_change[0]['cooldown_time_instant_mode'] = cooldown
        return True

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
                return True
        return False

    def SwitchStartUpWait(self):
        if instance.startUpWait:
            instance.startUpWait = False
        else:
            instance.startUpWait = True

    def SwitchShouldWaitAfterLogout(self, val=None):
        if instance.shouldWait:
            instance.shouldWait = False
        else:
            instance.shouldWait = True

    def SwitchUpgradeSkills(self):
        if instance.upgrade_skills:
            instance.upgrade_skills = False
        else:
            instance.upgrade_skills = True

    def SwitchUpgradeStats(self):
        if instance.upgrade_stats:
            instance.upgrade_stats = False
        else:
            instance.upgrade_stats = True

    def SwitchFollowVID(self):
        if instance.following_vid:
            instance.following_vid = False
        else:
            instance.following_vid = True

    def SwitchInstantMode(self, val=None):
        if instance.instant_mode:
            instance.instant_mode = False
        else:
            instance.instant_mode = True

    def SwitchUnmountHorse(self):
        if instance.unmount_horse:
            instance.unmount_horse = False
        else:
            instance.unmount_horse = True

    def SetUpgradeOrder(self, skill_id, new_order):
        skill_with_old_order = [skill for skill in instance.currentSkillSet if skill['upgrade_order'] == new_order]
        skill_to_change = [skill for skill in instance.currentSkillSet if skill['id'] == skill_id]
        if not skill_with_old_order or not skill_to_change:
            return False
        DebugPrint(str(skill_to_change[0]['upgrade_order']) + str(skill_with_old_order[0]['upgrade_order']))
        skill_with_old_order[0]['upgrade_order'], skill_to_change[0]['upgrade_order'] = \
            skill_to_change[0]['upgrade_order'], skill_with_old_order[0]['upgrade_order']
        DebugPrint(str(skill_with_old_order[0]['upgrade_order'])+ str(skill_to_change[0]['upgrade_order']))
        return True

skillbot_interface = SkillbotInterface()

