from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
import ui, player, net, m2netm2g, uiCharacter, chr
from OpenBot.Modules import OpenLib, Hooks
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
from OpenBot.Modules.Actions import ActionFunctions
import skill as m_skill

def __PhaseChangeSkillCallback(phase,phaseWnd):
    global instance
    if phase == OpenLib.PHASE_GAME:
        instance.resetSkills()
        OpenLib.SetTimerFunction(4, file_handler_interface.load_last_skills)
        if instance.shouldWait:
            instance.startUpWait = True

ADD_POINT = {
            "HP": "HP",
            "INT": "INT",
            "STR": "STR",
            "DEX": "DEX",
        }

class Skillbot(ui.ScriptWindow):

    ACTIVE_SKILL_IDS = [
        109,
        110,
        111,
        174,
        175,
        19,
        34,
        49,
        63,
        64,
        65,
        78,
        79,
        94,
        95,
        96,
        3,
        4,
    ]

    def __init__(self):
        ui.Window.__init__(self)
        self.enabled = False
        self.shouldWait = False
        self.startUpWait = False
        self.instant_mode = False
        self.upgrade_stats = False
        self.upgrade_skills = False
        self.following_vid = False
        self.unmount_horse = False
        self.followed_vid = 0
        self.stat_to_upgrade_order = ['DEX', 'STR', 'INT', 'HP']
        self.skill_to_upgrade_order = []
        self.currentSkillSet = []

        self.currActionDone = True
        self.lastTime = 0
        self.lastTimeUpgradedSkills = 0
        self.TimeToWaitAfterStart = 0
        self.lastTimeStartUp = 0
        self.chrwindow = uiCharacter.CharacterWindow()
        self.add_stat = self.chrwindow._CharacterWindow__OnClickStatusPlusButton


        self.resetSkills()

    def onStart(self):
        self.enabled = True

    def onStop(self):
        self.enabled = False

    def resetSkills(self):
        current_class = OpenLib.GetClass()
        if current_class == OpenLib.SKILL_SET_NONE:
            return
        skillIds = OpenLib.GetClassSkillIDs(current_class)
        self.currentSkillSet = []
        for i, id in enumerate(skillIds):
            self.currentSkillSet.append({
                'id': id,
                'can_cast': False,
                'cooldown_time_instant_mode': 0,
                'slot': i + 1,
                'is_turned_on': False,
                'upgrade_order': i+1,
                'lastWait': 0,
            })

    def addCallbackToWaiter(self, skill):
        def wait_to_use_skill():
            skill['is_turned_on'] = False

        return wait_to_use_skill

    def GetRawStatsDict(self):
        return {
            'HP': net.GetAccountCharacterSlotDataInteger(0, m2netm2g.ACCOUNT_CHARACTER_SLOT_CON),
            'INT': net.GetAccountCharacterSlotDataInteger(0, m2netm2g.ACCOUNT_CHARACTER_SLOT_INT),
            'STR': net.GetAccountCharacterSlotDataInteger(0, m2netm2g.ACCOUNT_CHARACTER_SLOT_STR),
            'DEX': net.GetAccountCharacterSlotDataInteger(0, m2netm2g.ACCOUNT_CHARACTER_SLOT_DEX),
        }

    def set_curr_action_done(self):
        self.currActionDone = True

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
        if val and OpenLib.IsInGamePhase() and self.enabled:

            statusPoint = player.GetStatus(player.STAT)
            if statusPoint and self.upgrade_stats:
                stats_dict = self.GetRawStatsDict()
                for stat in self.stat_to_upgrade_order:
                    if stats_dict[stat] < 90:
                        self.add_stat(stat)
                        break

            statusPoint = player.GetStatus(player.SKILL_ACTIVE)
            val, self.lastTimeUpgradedSkills = OpenLib.timeSleep(self.lastTimeUpgradedSkills, 2)
            if statusPoint and self.upgrade_skills and val:
                for _skill in sorted(self.currentSkillSet, key=lambda item: item['upgrade_order']):
                    if not player.GetSkillGrade(_skill['slot']) and player.GetSkillLevel(_skill['slot']) < 17:

                        self.chrwindow._CharacterWindow__SelectSkillGroup(net.GetMainActorSkillGroup()-1)
                        active_skill_obj = self.chrwindow.GetChild("Skill_Active_Slot")
                        active_skill_obj.eventPressedSlotButton(_skill['slot'])
                        break

            # Following target vid
            if self.following_vid and self.followed_vid and self.currActionDone:
                x, y, z = chr.GetPixelPosition(self.followed_vid)
                if not OpenLib.isPlayerCloseToPosition(x, y, 1000):
                    action = {
                        'name': '[Skillbot] - Walking to selected instance ' + chr.GetNameByVID(self.followed_vid),
                        'function_args': [[x, y]],
                        'function': ActionFunctions.MoveToPosition,
                        'callback': self.set_curr_action_done,
                    }
                    self.currActionDone = False
                    action_bot_interface.AddAction(action)
                    return

            if self.currActionDone:
                # This is for using skills
                character_class = OpenLib.GetClass()
                if not character_class:
                    return

                for skill in self.currentSkillSet:

                    val, skill['lastWait'] = OpenLib.timeSleep(skill['lastWait'], skill['cooldown_time_instant_mode'])
                    if val and skill['can_cast']:
                        skill['cooldown_time_instant_mode'] = m_skill.GetSkillCoolTime(skill['slot']) + 2
                        if self.unmount_horse and player.IsMountingHorse():
                            net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE_DOWN)

                        if not player.IsMountingHorse():
                            player.ClickSkillSlot(skill['slot'])

                        if self.unmount_horse and not player.IsMountingHorse():
                            net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE)

    def __del__(self):
        ui.Window.__del__(self)
        Hooks.deletePhaseCallback("skillCallback")

    def GetCurrentSkillSet(self):
        return self.currentSkillSet

instance = Skillbot()
instance.Show()
Hooks.registerPhaseCallback("skillCallback", __PhaseChangeSkillCallback)