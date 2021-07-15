import UIComponents
from BotBase import BotBase
import ui, chat, player, net
import OpenLib, eXLib
import Hooks




def __PhaseChangeSkillCallback(phase):
    global instance
    if phase == OpenLib.PHASE_GAME:
        instance.resetSkillsUI()


class Skillbot(BotBase):

    def __init__(self):
        BotBase.__init__(self)
        groupSkill = OpenLib.GetClass()

        self.currentSkillSet = []

        self.BuildWindow()
        self.resetSkillsUI()

    def BuildWindow(self):

        self.comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 255)
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
                                             funcState=self._start, defaultValue=False)



    def resetSkillsUI(self):
        current_class = OpenLib.GetClass()
        if(current_class == OpenLib.SKILL_SET_NONE):
            return
        skillIds = OpenLib.GetClassSkillIDs(current_class)
        del self.currentSkillSet[:]
        self.currentSkillSet = []
        for i,id in enumerate(skillIds):
            self.currentSkillSet.append({
                "icon":self.comp.OnOffButton(self.Board, '','', 15+ 35*i, 100,image=OpenLib.GetSkillIconPath(id)),
                "id":id,
                "slot":i+1,
            })


    def _start(self, val):
        if val:
            self.Start()
        else:
            self.Stop()


    def Frame(self):
        for skill in self.currentSkillSet:
            if not player.IsSkillCoolTime(skill['slot']) and skill['icon'].isOn:
                if not player.IsMountingHorse():
                    chat.AppendChat(3,"[Skill-Bot] Using skill at slot "+str(skill['slot']))
                    eXLib.SendUseSkillPacketBySlot(skill['slot'], player.GetTargetVID())


    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()


    def __del__(self):
        Hooks.deletePhaseCallback("skillCallback")


def switch_state():
    instance.switch_state()

instance = Skillbot()
Hooks.registerPhaseCallback("skillCallback",__PhaseChangeSkillCallback)