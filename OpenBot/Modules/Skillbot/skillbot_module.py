from OpenBot.Modules.OpenLog import DebugPrint
import ui, chat, player, net, m2netm2g,eXLib
from OpenBot.Modules import OpenLib, FileManager, Hooks
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface


def __PhaseChangeSkillCallback(phase,phaseWnd):
    global instance
    if phase == OpenLib.PHASE_GAME:
        instance.resetSkills()
        instance.LoadSettings()
        if instance.shouldWait:
            instance.startUpWait = True


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
        self.lastTime = 0
        self.enabled = False
        self.lastTimeStartUp = 0
        self.TimeToWaitAfterStart = 0
        self.shouldWait = False
        self.startUpWait = False
        self.instant_mode = False
        self.currentSkillSet = []

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
            if id in self.ACTIVE_SKILL_IDS:
                self.currentSkillSet.append({
                    'id': id,
                    'can_cast': False,
                    'cooldown_time_instant_mode': 0,
                    'slot': i + 1,
                    'is_turned_on': False,
                })
        #DebugPrint(str(self.currentSkillSet))

    def addCallbackToWaiter(self, skill):
        def wait_to_use_skill():
            skill['is_turned_on'] = False

        return wait_to_use_skill

    def OnUpdate(self):
        # USE player.ClickSkillSlot instead of SendUseSkillPacket for sura
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
        if val and OpenLib.IsInGamePhase() and self.enabled:
            if not self.startUpWait:
                for skill in self.currentSkillSet:
                    if self.instant_mode:
                        if not skill['is_turned_on'] and skill['can_cast'] and not player.IsSkillCoolTime(skill['slot']):
                            if not player.IsMountingHorse():
                                eXLib.SendUseSkillPacket(skill['id'], net.GetMainActorVID())
                            else:
                                net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE_DOWN)
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
                                eXLib.SendUseSkillPacketBySlot(skill['slot'])
                                net.SendCommandPacket(m2netm2g.PLAYER_CMD_RIDE)
            else:
                val, self.startUpWaitTime = OpenLib.timeSleep(self.startUpWaitTime, self.TimeToWaitAfterStart)
                if val:
                    self.startUpWait = False

    def __del__(self):
        ui.Window.__del__(self)
        Hooks.deletePhaseCallback("skillCallback")

    def GetCurrentSkillSet(self):
        return self.currentSkillSet

instance = Skillbot()
instance.Show()
Hooks.registerPhaseCallback("skillCallback", __PhaseChangeSkillCallback)