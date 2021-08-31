import UIComponents
from BotBase import BotBase
import ui, chat, player, net, m2netm2g
import OpenLib, eXLib, FileManager
import Hooks
from OpenBot.Modules.Actions import ActionBot
from OpenBot.Modules.Skillbot.skillbot_interface import instance as skillbot_interface


def __PhaseChangeSkillCallback(phase):
    global instance
    if phase == OpenLib.PHASE_GAME:
        instance.resetSkillsUI()
        instance.LoadSettings()
        if instance.shouldWait:
            instance.startUpWait = True
        if instance.enableButton.isOn:
            instance.Start()
        else:
            instance.Stop()


class Skillbot(BotBase):

    def __init__(self):
        BotBase.__init__(self)
        self.BuildWindow()

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        status = skillbot_interface.GetStatus()

        self.comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 150)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Skillbot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        self.enableButton = self.comp.OnOffButton(self.Board, '', '', 15, 40,
                                                  OffUpVisual='OpenBot/Images/start_0.tga',
                                                  OffOverVisual='OpenBot/Images/start_1.tga',
                                                  OffDownVisual='OpenBot/Images/start_2.tga',
                                                  OnUpVisual='OpenBot/Images/stop_0.tga',
                                                  OnOverVisual='OpenBot/Images/stop_1.tga',
                                                  OnDownVisual='OpenBot/Images/stop_2.tga',
                                                  funcState=self._start, defaultValue=status['Enabled'])

        self.showShouldWaitButton = self.comp.OnOffButton(self.Board, '\t\t\t\t\t\tWait after logout?',
                                                          'If check, skillbot will wait to use skill', 15, 95,
                                                          funcState=skillbot_interface.SwitchShouldWaitAfterLogout,
                                                          defaultValue=status['ShouldWaitAfterLogout'])

        self.slotBarSlot, self.edit_lineWaitingTime = self.comp.EditLine(self.Board,
                                                                         str(status['TimeToWaitAfterLogout']),
                                                                         15, 117, 25, 15, 25)

        self.text_line1 = self.comp.TextLine(self.Board, 's. waiting after logout', 50, 118,
                                             self.comp.RGB(255, 255, 255))

        self.showModeButton = self.comp.OnOffButton(self.Board, '\t\t\t\tCast instant?', 'Not working with every class',
                                                    120, 95,
                                                    funcState=skillbot_interface.SwitchInstantMode,
                                                    defaultValue=status['InstantMode'])
        pos_x = 0
        for skill in status['CurrentSkillSet']:
            button = self.comp.OnOffButton(self.Board, '', '', 75 + 35 * pos_x, 45,
                                           image=OpenLib.GetSkillIconPath(skill['id']),
                                           funcState=self.create_switch_function(skill['id']))
            slot_bar, edit_line = self.comp.EditLine(self.Board, '40', 78 + 35 * pos_x, 75, 25, 15, 25)
            setattr(self, 'button' + str(id), button)
            setattr(self, 'slot_bar' + str(id), slot_bar)
            setattr(self, 'edit_line' + str(id), edit_line)
            pos_x += 1

    def create_switch_function(self, skill_id):

        def x():
            skillbot_interface.SwitchSkill(skill_id)

        return x

    def SaveSettings(self):
        if not skillbot_interface.SaveSettings():
            chat.AppendChat(3, '[Skillbot] - Cannot save settings')

    def LoadSettings(self):
        if not skillbot_interface.LoadSettings():
            chat.AppendChat(3, '[Skillbot] - Cannot load settings')

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
            self.Board.Hide()
        else:
            self.Board.Show()

    def __del__(self):
        Hooks.deletePhaseCallback("skillCallback")

    def Frame(self):
        status = skillbot_interface.GetStatus()
        for skill in status['CurrentSkillSet']:
            time_to_wait = getattr(self, 'edit_line'+str(skill['id']))
            if self.is_text_validate(time_to_wait):
                skillbot_interface.SetCooldownForSkill(skill['id'], time_to_wait)

def switch_state():
    instance.switch_state()


instance = Skillbot()
Hooks.registerPhaseCallback("skillCallback", __PhaseChangeSkillCallback)