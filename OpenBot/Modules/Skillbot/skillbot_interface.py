from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Skillbot.skillbot_module import instance
from OpenBot.Modules import OpenLib

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
    'STAT_TO_UPGRADE_ORDER': 'StatToUpgradeOrder',
    'USE_ONLY_IF_ATTACKER_IS_RUNNING': 'UseOnlyIfAttackerIsRunning',
}

class SkillbotInterface:

    def SetStatus(self, status, save_status=True):
        for status_key in status.keys():
            if STATUS['ENABLED'] == status_key:
                self.SwitchEnabled()
            elif STATUS['TIME_TO_WAIT_AFTER_LOGOUT'] == status_key:
                self.SetTimeToWaitAfterLogout(status_key)

            elif STATUS['SHOULD_WAIT_AFTER_LOGOUT'] == status_key:
                self.SwitchShouldWaitAfterLogout()

            elif STATUS['INSTANT_MODE'] == status_key:
                self.SwitchInstantMode()

            elif STATUS['UPGRADE_SKILLS'] == status_key:
                self.SwitchUpgradeSkills()

            elif STATUS['UPGRADE_STATES'] == status_key:
                self.SwitchUpgradeStats()

            elif STATUS['FOLLOW_VID'] == status_key:
                self.SwitchFollowVID()

            elif STATUS['FOLLOWED_VID'] == status_key:
                instance.followed_vid = status[status_key]

            elif STATUS['UNMOUNT_HORSE'] == status_key:
                instance.unmount_horse = status[status_key]

            elif STATUS['STAT_TO_UPGRADE_ORDER'] == status_key:
                instance.stat_to_upgrade_order = status[status_key]

            elif STATUS['USE_ONLY_IF_ATTACKER_IS_RUNNING'] == status_key:
                instance.use_skills_only_if_attacker_is_running = status[status_key]


        if OpenLib.GetClass() != OpenLib.SKILL_SET_NONE:
            if not len(instance.currentSkillSet):
                instance.resetSkills()

            skill_ids = OpenLib.GetClassSkillIDs(OpenLib.GetClass())
            for index in range(len(instance.currentSkillSet)):
                if instance.currentSkillSet[index]['id'] != skill_ids[index]:
                    instance.resetSkills()
                    break

            if STATUS['CURRENT_SKILL_SET'] in status.keys():
                for skill in range(len(status['CurrentSkillSet'])):
                    if status['CurrentSkillSet'][skill]['id'] != instance.currentSkillSet[skill]['id']:
                        instance.resetSkills()
                        break

                    if status['CurrentSkillSet'][skill]['can_cast'] != instance.currentSkillSet[skill]['can_cast']:
                        self.SwitchSkill(status['CurrentSkillSet'][skill]['id'])
                    if status['CurrentSkillSet'][skill]['cooldown_time_instant_mode'] != instance.currentSkillSet[skill]['cooldown_time_instant_mode']:
                        self.SetCooldownForSkill(status['CurrentSkillSet'][skill]['id'], status['CurrentSkillSet'][skill]['cooldown_time_instant_mode'])
                    if status['CurrentSkillSet'][skill]['upgrade_order'] != instance.currentSkillSet[skill]['upgrade_order']:
                        self.SetUpgradeOrder(status['CurrentSkillSet'][skill]['id'], status['CurrentSkillSet'][skill]['upgrade_order'])
                    if status['CurrentSkillSet'][skill]['use_metin_cooldown'] != instance.currentSkillSet[skill]['use_metin_cooldown']:
                        self.SetUpgradeOrder(status['use_metin_cooldown'][skill]['id'], status['CurrentSkillSet'][skill]['use_metin_cooldown'])
        if save_status: self.SaveStatus()

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
            STATUS['STAT_TO_UPGRADE_ORDER']: instance.stat_to_upgrade_order,
            STATUS['USE_ONLY_IF_ATTACKER_IS_RUNNING']: instance.use_skills_only_if_attacker_is_running,
        }

    def SaveStatus(self):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        file_handler_interface.dump_other_settings()

    def Start(self):
        instance.onStart()

    def Stop(self):
        instance.onStop()

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

    def SwitchEnabled(self):
        if instance.enabled:
            self.Stop()
        else:
            self.Start()

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
        skill_with_old_order[0]['upgrade_order'], skill_to_change[0]['upgrade_order'] = \
            skill_to_change[0]['upgrade_order'], skill_with_old_order[0]['upgrade_order']
        return True

skillbot_interface = SkillbotInterface()

