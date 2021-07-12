import UIComponents
from BotBase import BotBase
import ui, chat, player, net
import OpenLib, eXLib

warriorBody = [
    {'id': 4, 'name': 'Aura of the sword', 'image_str': str('d:/ymir work/ui/skill/warrior/geomgyeong_03.sub')}, # palbang wir miecz # samyeon 3krotne ciecie gyeoksan walniecie gigongcham ?? geompung uderzenie miecza
    {'id': 3, 'name': 'Berserk', 'image_str': str('d:/ymir work/ui/skill/warrior/jeongwi_03.sub')}   # cheongeun silne daejin tapniecie jeongwi berserk tanhwan sarza geomgyeong aura
]
warriorMental = [
    {'id': 19, 'name': 'Strong body', 'image_str': str('d:/ymir work/ui/skill/warrior/cheongeun_03.sub')},
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
ninjaArcher = [
    {'id':49, 'name': 'Feather walk'},
]
shamanDragon = [
    {'id': 109, 'name': 'Blessing'},
    {'id': 110, 'name': 'Reflect'},
    {'id': 111, 'name': 'Dragons Strength'}
]
shamanHeal = [
    {'id': 94, 'name': 'Cure'},
    {'id': 95, 'name': 'Swiftness'},
    {'id': 96, 'name': 'Attack up'},
]
lycan_1, lycan_2 = [], []


class Skillbot(BotBase):

    def __init__(self):
        BotBase.__init__(self)
        groupSkill = OpenLib.GetClass()
        self.current_skill_set = {}
        self.skills_buttons_names = []
        if groupSkill == OpenLib.SKILL_SET_BODY_WARRIOR:
            self.current_skill_set = warriorBody
        elif groupSkill == OpenLib.SKILL_SET_MENTAL_WARRIOR:
            self.current_skill_set = warriorMental
        elif groupSkill == OpenLib.SKILL_SET_ARCHER_NINJA:
            self.current_skill_set = ninjaArcher
        elif groupSkill == OpenLib.SKILL_SET_DAGGER_NINJA:
            self.current_skill_set = ninjaDagger
        elif groupSkill == OpenLib.SKILL_SET_WEAPONS_SURA:
            self.current_skill_set = suraWP
        elif groupSkill == OpenLib.SKILL_SET_MAGIC_SURA:
            self.current_skill_set = suraBM
        elif groupSkill == OpenLib.SKILL_SET_DRAGON_SHAMAN:
            self.current_skill_set = shamanDragon
        elif groupSkill == OpenLib.SKILL_SET_HEAL_SHAMAN:
            self.current_skill_set = shamanHeal
        elif groupSkill == OpenLib.SKILL_SET_1_LYCAN:
            self.current_skill_set = lycan_1
        elif groupSkill == OpenLib.SKILL_SET_2_LYCAN:
            self.current_skill_set = lycan_2
        self.BuildWindow()

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
            skill_name = 'skill'+str(self.current_skill_set[skill]['id'])
            image = comp.ExpandedImage(self.Board, 80, 40+(skill*60), self.current_skill_set[skill]['image_str'])
            setattr(self, skill_name+'Image', image)
            button = comp.OnOffButton(self.Board, '\t\t\t\t\t\t' + self.current_skill_set[skill]['name'],
                                      '', 100, 58+(skill*60), defaultValue=False)





            self.skills_buttons_names.append(skill_name)
            setattr(self, skill_name, button)
            setattr(self, skill_name+'LastTime', 10)

            slot_bar, edit_line = comp.EditLine(self.Board, str(0), 80, 72+(skill*60), 40, 18, 25)
            setattr(self, skill_name+'SlotBar', slot_bar)
            setattr(self, skill_name+'EditLine', edit_line)

            text = comp.TextLine(self.Board, 's. delay time', 130, 77+(skill*60), comp.RGB(255, 255, 255))
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
                val, skill_last_time = OpenLib.timeSleep(skill_last_time, int(text))
                if val:
                    setattr(self, skill_name+'LastTime', skill_last_time)
                    if not player.IsSkillCoolTime(skill_dict['id']):
                        if not player.IsMountingHorse():
                            eXLib.SendUseSkillPacket(skill_dict['id'], 0)
                        else:
                            player.ClickSkillSlot(9)
                            eXLib.SendUseSkillPacket(skill_dict['id'], 0)
                            player.ClickSkillSlot(9)

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

