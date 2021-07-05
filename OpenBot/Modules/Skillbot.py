from UIComponents import Component
from BotBase import BotBase
import ui, chat, player
import OpenLib, eXLib

warriorBody = [
    {'id': 1, 'name': '3-way cut', 'is_buff': False},
    {'id': 2, 'name': 'Sword spin', 'is_buff': False},
    {'id': 3, 'name': 'Dash', 'is_buff': False},
    {'id': 4, 'name': 'Aura of the sword', 'is_buff': True},
    {'id': 5, 'name': 'Berserk', 'is_buff': True}
]
warriorMental = {
    16: 'Spirit strike',
    17: 'Bash',
    18: 'Stump',
    19: 'Strong body',
    20: 'Sword strike'
}
suraWP = {
    61: 'Finger strike',
    62: 'Dragon swirl',
    63: 'Enchanted blade',
    64: 'Fear',
    65: 'Enchanted Armour'
}
suraBM = {
    76: 'Dark strike',
    77: 'Flame strike',
    78: 'Flame spirit',
    79: 'Dark protection',
    80: 'Spirit Strike',
    81: 'Dark orb'
}
ninjaDagger = {
    31: 'Ambush',
    32: 'Fast attack',
    33: 'Rolling dagger',
    34: 'Stealth',
    35: 'Poisonous cloud'
}
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
        if groupSkill == 1:
            self.current_skill_set = warriorBody
        self.BuildWindow()

    def BuildWindow(self):

        comp = Component()
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

        if self.current_skill_set[0]['is_buff']:
            self.skillOne = comp.OnOffButton(self.Board,
                                             '\t\t\t\t\t\t' + self.current_skill_set[0]['name'],
                                             '', 40, 40, defaultValue=False)
        if self.current_skill_set[1]['is_buff']:
            self.skillTwo = comp.OnOffButton(self.Board,
                                             '\t\t\t\t\t\t' + self.current_skill_set[1]['name'],
                                             '', 40, 60, defaultValue=False)
        if self.current_skill_set[2]['is_buff']:
            self.skillThree = comp.OnOffButton(self.Board,
                                           '\t\t\t\t\t\t' + self.current_skill_set[2]['name'],
                                           '', 40, 80, defaultValue=False)
        if self.current_skill_set[3]['is_buff']:
            self.skillFour = comp.OnOffButton(self.Board,
                                              '\t\t\t\t\t\t' + self.current_skill_set[3]['name'],
                                              '', 40, 100, defaultValue=False)
        if self.current_skill_set[4]['is_buff']:
            self.skillFive = comp.OnOffButton(self.Board,
                                              '\t\t\t\t\t\t' + self.current_skill_set[4]['name'],
                                              '', 40, 120, defaultValue=False)

        if len(self.current_skill_set) > 5:
            if self.current_skill_set[5]['is_buff']:
                self.skillSix = comp.OnOffButton(self.Board,
                                                 '\t\t\t\t\t\t' + self.current_skill_set[5]['name'],
                                                 '', 40, 140, defaultValue=False)

    def _start(self, val):
        if val:
            self.Start()
        else:
            self.Stop()

    def Frame(self):
        if self.current_skill_set[0]['is_buff']:
            if self.skillOne.isOn:
                if not player.IsSkillCoolTime(self.current_skill_set[0]['id']):
                    eXLib.SendUseSkillPacket(self.current_skill_set.keys[0]['id'], 0)

        if self.current_skill_set[1]['is_buff']:
            if self.skillTwo.isOn:
                if not player.IsSkillCoolTime(self.current_skill_set[1]['id']):
                    eXLib.SendUseSkillPacket(self.current_skill_set[1]['id'], 0)

        if self.current_skill_set[2]['is_buff']:
            if self.skillTree.isOn:
                if not player.IsSkillCoolTime(self.current_skill_set[2]['id']):
                    eXLib.SendUseSkillPacket(self.current_skill_set[2]['id'], 0)

        if self.current_skill_set[3]['is_buff']:
            if self.skillFour.isOn:
                if not player.IsSkillCoolTime(self.current_skill_set[3]['id']):
                    eXLib.SendUseSkillPacket(self.current_skill_set[3]['id'], 0)

        if self.current_skill_set[4]['is_buff']:
            if self.skillFive.isOn:
                if not player.IsSkillCoolTime(self.current_skill_set[4]['id']):
                    player.ClickSkillSlot(3)
                    #eXLib.SendUseSkillPacket(self.current_skill_set[4]['id'], 0)

        if len(self.current_skill_set) > 5:
            if self.current_skill_set[5]['is_buff']:
                if self.skillSix.isOn:
                    if not player.IsSkillCoolTime(self.current_skill_set[5]['id']):
                        eXLib.SendUseSkillPacket(self.current_skill_set[5]['id'], 0)

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

