from OpenBot.Modules import UIComponents, OpenLib, Hooks, OpenLog
import ui, chat
from OpenBot.Modules.Skillbot.skillbot_interface import interface as skillbot_interface


def __PhaseChangeSkillCallback(phase):
    global instance
    if phase == OpenLib.PHASE_GAME:
        skillbot_interface.ResetSkills()
        skillbot_interface.LoadSettings()
        if skillbot_interface.GetStatus()['ShouldWaitAfterLogout']:
            skillbot_interface.SwitchStartUpWait()
        if instance.enableButton.isOn:
            skillbot_interface.Start()
        else:
            skillbot_interface.Stop()


class Skillbot(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.BuildWindow()

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        self.comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 150)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Skillbot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        status = skillbot_interface.GetStatus()
        OpenLog.DebugPrint(str(status))

        self.enableButton = self.comp.OnOffButton(self.Board, '', '', 15, 40,
                                                  OffUpVisual='OpenBot/Images/start_0.tga',
                                                  OffOverVisual='OpenBot/Images/start_1.tga',
                                                  OffDownVisual='OpenBot/Images/start_2.tga',
                                                  OnUpVisual='OpenBot/Images/stop_0.tga',
                                                  OnOverVisual='OpenBot/Images/stop_1.tga',
                                                  OnDownVisual='OpenBot/Images/stop_2.tga',
                                                  funcState=self._start, defaultValue=False)

        self.showShouldWaitButton = self.comp.OnOffButton(self.Board, '\t\t\t\t\t\tWait after logout?',
                                                          'If check, skillbot will wait to use skill', 15, 95,
                                                          funcState=skillbot_interface.SwitchShouldWaitAfterLogout,
                                                          defaultValue=False)

        self.slotBarSlot, self.edit_lineWaitingTime = self.comp.EditLine(self.Board,
                                                                         str(status['TimeToWaitAfterLogout']),
                                                                         15, 117, 25, 15, 25)

        self.text_line1 = self.comp.TextLine(self.Board, 's. waiting after logout', 50, 118,
                                             self.comp.RGB(255, 255, 255))

        self.showModeButton = self.comp.OnOffButton(self.Board, '\t\t\t\tCast instant?', 'Not working with every class',
                                                    120, 95,
                                                    funcState=skillbot_interface.SwitchInstantMode,
                                                    defaultValue=False)

    def CreateSkillSet(self):
        pos_x = 0
        self.LoadSettings()
        status = skillbot_interface.GetStatus()
        for skill in status['CurrentSkillSet']:
            button = self.comp.OnOffButton(self.Board, '', '', 75 + 35 * pos_x, 45,
                                           image=OpenLib.GetSkillIconPath(skill['id']),
                                           funcState=self.create_switch_function(skill['id']), defaultValue=False)
            slot_bar, edit_line = self.comp.EditLine(self.Board, str(skill['cooldown_time_instant_mode']), 78 + 35 * pos_x, 75, 25, 15, 25)

            OpenLog.DebugPrint(str(skill['can_cast']))
            if skill['can_cast']:
                if not button.isOn:
                    button.SetOn()
            else:
                if button.isOn:
                    button.SetOff()

            setattr(self, 'button' + str(skill['id']), button)
            setattr(self, 'slot_bar' + str(skill['id']), slot_bar)
            setattr(self, 'edit_line' + str(skill['id']), edit_line)
            pos_x += 1

    def create_switch_function(self, skill_id):

        def x(val):
            OpenLog.DebugPrint('if this asdflhkjasfdafdssfdfdsasafd')
            result = skillbot_interface.SwitchSkill(skill_id)
            if not result:
                chat.AppendChat(3, '[Skillbot] - Cannot launch skill')

        return x

    def SaveSettings(self):
        if not skillbot_interface.SaveSettings():
            chat.AppendChat(3, '[Skillbot] - Cannot save settings')

    def LoadSettings(self):
        if not skillbot_interface.LoadSettings():
            chat.AppendChat(3, '[Skillbot] - Cannot load settings')
        status = skillbot_interface.GetStatus()
        OpenLog.DebugPrint(str(status))
        if status['InstantMode']:
            self.showModeButton.SetOn()
        else:
            self.showModeButton.SetOff()

        if status['Enabled']:
            self.enableButton.SetOn()
        else:
            self.enableButton.SetOff()
        
        if status['ShouldWaitAfterLogout']:
            self.showShouldWaitButton.SetOn()
        else:
            self.showShouldWaitButton.SetOff()

    def _start(self, val):
        if val:
            skillbot_interface.Start()
        else:
            skillbot_interface.Stop()

    def is_text_validate(self, text):
        try:
            int(text)
        except ValueError:
            chat.AppendChat(3, '[Skillbot] - The value must be a digit')
            return False
        if int(text) < 0:
            chat.AppendChat(3, '[Skillbot] - The value must be in range 0 to infinity')
            return False
        return True

    def switch_state(self):
        if self.Board.IsShow():
            self.SaveSettings()
            self.Board.Hide()
        else:
            self.CreateSkillSet()
            self.Board.Show()

    def __del__(self):
        Hooks.deletePhaseCallback("skillCallback")

    def OnUpdate(self):
        status = skillbot_interface.GetStatus()
        for skill in status['CurrentSkillSet']:
            try:
                time_to_wait = getattr(self, 'edit_line'+str(skill['id'])).GetText()
            except AttributeError:
                continue
            if self.is_text_validate(time_to_wait):
                skillbot_interface.SetCooldownForSkill(skill['id'], int(time_to_wait))
            else:
                chat.AppendChat(3, 'Cannot set cooldown')


instance = Skillbot()
instance.Show()
Hooks.registerPhaseCallback("skillCallback", __PhaseChangeSkillCallback)