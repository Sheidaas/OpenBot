from OpenBot.Modules.OpenLog import DebugPrint
import ui, player, net, m2netm2g, uiCharacter, chr
import skill as metin_skill
from OpenBot.Modules import OpenLib, FileManager, Hooks
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
from OpenBot.Modules.Actions import ActionFunctions

def __PhaseChangeSkillCallback(phase,phaseWnd):
    global instance
    if phase == OpenLib.PHASE_GAME:
        instance.resetSkills()
        instance.LoadSettings()
        if instance.shouldWait:
            instance.startUpWait = True

ADD_POINT = {
            "HP": "HP",
            "INT": "INT",
            "STR": "STR",
            "DEX": "DEX",
        }
"""
       # USE player.ClickSkillSlot instead of SendUseSkillPacket for sura
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
        if val and OpenLib.IsInGamePhase() and self.enabled:
            if not self.startUpWait:
                for skill in self.currentSkillSet:
                    if self.instant_mode:
                        if not skill['is_turned_on'] and skill['can_cast'] and not player.IsSkillCoolTime(skill['slot']):
                                eXLib.SendUseSkillPacket(skill['id'], net.GetMainActorVID())
                            else:
                                eXLib.SendUseSkillPacket(skill['id'], net.GetMainActorVID())
                                net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE)
                            skill['is_turned_on'] = True
                            action_bot_interface.AddWaiter(skill['cooldown_time_instant_mode'], self.addCallbackToWaiter(skill))
                    else:
                        if not skill['is_turned_on'] and skill['can_cast'] and not player.IsSkillCoolTime(skill['slot']):
                            if not player.IsMountingHorse():
                                eXLib.SendUseSkillPacketBySlot(skill['slot'])
                            else:
                                net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE_DOWN)
                                net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE)
            else:
                val, self.startUpWaitTime = OpenLib.timeSleep(self.startUpWaitTime, self.TimeToWaitAfterStart)
                if val:
                    self.startUpWait = False
"""
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
        self.TimeToWaitAfterStart = 0
        self.lastTimeStartUp = 0
        self.chrwindow = uiCharacter.CharacterWindow()
        self.add_stat = self.chrwindow._CharacterWindow__OnClickStatusPlusButton


        self.resetSkills()

    def onStart(self):
        self.enabled = True

    def onStop(self):
        self.enabled = False

    def SaveSettings(self, filename=''):
        for skill in self.currentSkillSet:
            FileManager.WriteConfig(str(skill['id']), str(skill['can_cast']), file=FileManager.CONFIG_SKILLBOT)
            FileManager.WriteConfig('skillTimer'+str(skill['id']), str(skill['cooldown_time_instant_mode']), file=FileManager.CONFIG_SKILLBOT)
        FileManager.WriteConfig('InstantMode', str(self.instant_mode), file=FileManager.CONFIG_SKILLBOT)
        FileManager.WriteConfig('IsTurnedOn', str(self.enabled), file=FileManager.CONFIG_SKILLBOT)
        FileManager.WriteConfig('ShouldWaitAfterLogout', str(self.shouldWait), file=FileManager.CONFIG_SKILLBOT)
        FileManager.WriteConfig('TimeToWaitAfterStart', str(self.TimeToWaitAfterStart), file=FileManager.CONFIG_SKILLBOT)
        FileManager.Save(file=FileManager.CONFIG_SKILLBOT)

    def LoadSettings(self, filename=''):
        self.enabled = FileManager.boolean(FileManager.ReadConfig('IsTurnedOn',
                                                                  file=FileManager.CONFIG_SKILLBOT))
        self.instant_mode = FileManager.boolean(FileManager.ReadConfig('InstantMode',
                                                                       file=FileManager.CONFIG_SKILLBOT))
        self.shouldWait = FileManager.boolean(FileManager.ReadConfig('ShouldWaitAfterLogout',
                                                                     file=FileManager.CONFIG_SKILLBOT))
        
        self.TimeToWaitAfterStart = int(FileManager.ReadConfig('TimeToWaitAfterStart',
                                                                     file=FileManager.CONFIG_SKILLBOT))

        for skill in self.currentSkillSet:
            skill['can_cast'] = FileManager.boolean(FileManager.ReadConfig(str(skill['id']),
                                                                           file=FileManager.CONFIG_SKILLBOT))
            skill['cooldown_time_instant_mode'] = int(FileManager.ReadConfig('skillTimer' + str(skill['id']),
                                                                         file=FileManager.CONFIG_SKILLBOT))
                                                                         

    def resetSkills(self):
        current_class = OpenLib.GetClass()
        if current_class == OpenLib.SKILL_SET_NONE:
            return
        skillIds = OpenLib.GetClassSkillIDs(current_class)
        self.currentSkillSet = []
        for i, id in enumerate(skillIds):
            #if id in self.ACTIVE_SKILL_IDS:
            self.currentSkillSet.append({
                'id': id,
                'can_cast': False,
                'cooldown_time_instant_mode': 0,
                'slot': i + 1,
                'is_turned_on': False,
                'upgrade_order': i+1,
                'lastWait': 0,
            })
        #DebugPrint(str(self.currentSkillSet))

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
            if statusPoint and self.upgrade_skills:
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

                        if self.unmount_horse and player.IsMountingHorse():
                            net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE_DOWN)

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