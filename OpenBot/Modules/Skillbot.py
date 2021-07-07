import UIComponents
from BotBase import BotBase
import ui, chat, player
import OpenLib, eXLib

warriorBody = [
    {'id': 4, 'name': 'Aura of the sword'},
    {'id': 3, 'name': 'Berserk'}
]
warriorMental = [
    {'id': 19, 'name': 'Strong body'},
]
suraWP = [
    {'id': 63, 'name': 'Enchanted blade'},
    {'id': 64, 'name': 'Fear'},
    {'id': 65, 'name': 'Enchanted Armour'}
]
suraBM = [
    {'id': 79, 'name': 'Dark protection'},
    {'id': 81, 'name': 'Dark orb'}
]
ninjaDagger = [
    {'id': 34, 'name': 'Stealth'},
]
ninjaArcher = {
    46: 'Repetitive shot',
    47: 'Arrow shower',
    48: 'Fire arrow',
    49: 'Feather walk',
    50: 'Poison arrow'
}
shamanDragon = {
    106: 'Flying Talisman',
    107: 'Shooting Dragon',
    108: 'Dragon Roar',
    109: 'Blessing',
    110: 'Reflect',
    111: 'Dragons Strength'
}
shamanHeal = {
    91: 'Lightning claw',
    92: 'Summon lightning',
    93: 'Lightning throw',
    94: 'Cure',
    95: 'Swiftness',
    96: 'Attack up',
}


class Skillbot(BotBase):

    def __init__(self):
        BotBase.__init__(self)
        raceName, groupSkill = OpenLib.GetClass()
        self.current_skill_set = {}
        self.skills_buttons_names = []
        if groupSkill == 1:
            self.current_skill_set = warriorBody
        self.BuildWindow()

    def render_many_buttons(self):
        pass

    def BuildWindow(self):

        comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 255)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Skillbot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        self.enableButton = comp.OnOffButton(self.Board, '', '', 15, 40,
                                             OffUpVisual='OpenBot/Images/start_0.tga',
                                             OffOverVisual='OpenBot/Images/start_1.tga',
                                             OffDownVisual='OpenBot/Images/start_2.tga',
                                             OnUpVisual='OpenBot/Images/stop_0.tga',
                                             OnOverVisual='OpenBot/Images/stop_1.tga',
                                             OnDownVisual='OpenBot/Images/stop_2.tga',
                                             funcState=self._start, defaultValue=False)

        for skill in range(len(self.current_skill_set)):
            button = comp.OnOffButton(self.Board, '\t\t\t\t\t\t' + self.current_skill_set[skill]['name'],
                                      '', 80, 40+(skill*40), defaultValue=False)
            skill_name = 'skill'+str(self.current_skill_set[skill]['id'])
            self.skills_buttons_names.append(skill_name)
            setattr(self, skill_name, button)
            setattr(self, skill_name+'LastTime', 0)

            slot_bar, edit_line = comp.EditLine(self.Board, str(0), 80, 56+(skill*40), 40, 18, 25)
            setattr(self, skill_name+'SlotBar', slot_bar)
            setattr(self, skill_name+'EditLine', edit_line)

            text = comp.TextLine(self.Board, 's. delay time', 130, 62+(skill*40), comp.RGB(255, 255, 255))
            setattr(self, skill_name+'EditLineText', text)

    def _start(self, val):
        if val:
            self.Start()
        else:
            self.Stop()

    def get_skill_dict_by_skill_name(self, skill_name):
        id = int(skill_name.strip('skill'))
        for skill in self.current_skill_set:
            if skill['id'] == id:
                return skill
        return False

    def Frame(self):
        for skill_name in self.skills_buttons_names:
            skill_button = getattr(self, skill_name)
            skill_dict = self.get_skill_dict_by_skill_name(skill_name)
            if skill_button.isOn:
                text = getattr(self, skill_name+'EditLine').GetText()
                if not self.is_text_validate(text):
                    self.enableButton.SetOff()
                    self.Stop()
                    return

                # Getting skill[id]LastTime
                skill_last_time = getattr(self, skill_name+'LastTime')
                chat.AppendChat(3, str(skill_last_time) + ','+str(text))
                val, skill_last_time = OpenLib.timeSleep(skill_last_time, int(text))
                if val:
                    setattr(self, skill_name+'LastTime', skill_last_time)
                    if not player.IsSkillCoolTime(skill_dict['id']):
                        eXLib.SendUseSkillPacket(skill_dict['id'], 0)

    def is_text_validate(self, text):
        try:
            int(text)
        except ValueError:
            chat.AppendChat(3, '[Skillbot] - The value must be a digit')
            return False
        if int(text) < 1:
            chat.AppendChat(3, '[Skillbot] - The value must be in range 1 to infinity')
            return False
        return True

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

