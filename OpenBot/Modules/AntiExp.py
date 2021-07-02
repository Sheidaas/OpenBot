from BotBase import BotBase
from UIComponents import Component
import OpenLib
import net, ui, chat


class AntiExp(BotBase):
    def __init__(self):
        BotBase.__init__(self, time_wait=4)

        self.BuildWindow()

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(125, 125)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('AntiExp')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = Component()
        self.enableButton = comp.OnOffButton(self.Board, '', '', 15, 50,
                                             OffUpVisual='OpenBot/Images/start_0.tga',
                                             OffOverVisual='OpenBot/Images/start_1.tga',
                                             OffDownVisual='OpenBot/Images/start_2.tga',
                                             OnUpVisual='OpenBot/Images/stop_0.tga',
                                             OnOverVisual='OpenBot/Images/stop_1.tga',
                                             OnDownVisual='OpenBot/Images/stop_2.tga',
                                             funcState=self._start, defaultValue=False)

    def _start(self, val):
        if val:
            self.Start()
        else:
            self.Stop()

    def Frame(self):
        status = OpenLib.getAllStatusOfMainActor()
        exp = status['EXP']
        if exp > 0:
            if exp < 1000000:
                net.SendGuildOfferPacket(exp)
            else:
                net.SendGuildOfferPacket(1000000)


    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()