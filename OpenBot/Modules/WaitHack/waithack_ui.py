from OpenBot.Modules import UIComponents
from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
import eXLib,ui,net,chr,player,chat,item,skill


class DmgHacksInstance(ui.Window):
    def __init__(self):
        ui.Window.__init__(self)
        self.BuildWindow()

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(300, 260)
        self.Board.SetCenterPosition()
        self.Board.AddFlag('movable')
        self.Board.AddFlag('float')
        self.Board.SetTitleName('WaitHack')
        self.Board.SetCloseEvent(self.Close)
        self.Board.Hide()
        self.comp = UIComponents.Component()

        status = waithack_interface.GetStatus()

        self.enableButton = self.comp.OnOffButton(self.Board, '', '', 130, 210, OffUpVisual=eXLib.PATH + 'OpenBot/Images/start_0.tga',
                                                                             OffOverVisual=eXLib.PATH + 'OpenBot/Images/start_1.tga',
                                                                              OffDownVisual=eXLib.PATH + 'OpenBot/Images/start_2.tga',
                                                                              OnUpVisual=eXLib.PATH + 'OpenBot/Images/stop_0.tga',
                                                                               OnOverVisual=eXLib.PATH + 'OpenBot/Images/stop_1.tga',
                                                                                OnDownVisual=eXLib.PATH + 'OpenBot/Images/stop_2.tga',
                                                                                funcState=self.OnOffBtnState, defaultValue=status['Enabled'])
        self.playerClose = self.comp.OnOffButton(self.Board, '', '', 130, 50)
        self.wallBtn = self.comp.OnOffButton(self.Board, '\t\t\t\tCheck is wall', 'Dont attack mobs with wall in between', 170, 30, funcState=waithack_interface.SwitchIsWallBetween,
        defaultValue=status['IsWallBetween'])
        self.cloudBtn = self.comp.OnOffButton(self.Board, '\t\t\t\tCloud exploit', 'Only on dagger ninja', 170, 50, funcState=waithack_interface.SwitchUseCloudExploit,
        defaultValue=status['UseCloudExploit'])
        self.attackPlayerBtn = self.comp.OnOffButton(self.Board, '\t\t\t\tAttack players', '', 170, 70, funcState=waithack_interface.SwitchAttackPlayer, defaultValue=status['AttackPlayer'])
        self.attackBlockedMonsters = self.comp.OnOffButton(self.Board, '\t\t\t\t', '', 130, 70,
        funcState=waithack_interface.SwitchAttackBlockedMonsters, defaultValue=status['AttackBlockedMonsters'])
        self.AttackBlockedMonsers = self.comp.TextLine(self.Board, 'Attack blocked monsters', 13, 70, self.comp.RGB(255, 255, 255))
        self.RangeLabel = self.comp.TextLine(self.Board, 'Range', 13, 102, self.comp.RGB(255, 255, 255))
        self.SpeedLabel = self.comp.TextLine(self.Board, 'Speed', 13, 136, self.comp.RGB(255, 255, 255))
        self.MonsterLabel = self.comp.TextLine(self.Board, 'Monsters', 13, 170, self.comp.RGB(255, 255, 255))
        self.PlayerLabel = self.comp.TextLine(self.Board, 'Stop when player close', 12, 51, self.comp.RGB(255, 255, 255))
        self.rangeNum = self.comp.TextLine(self.Board, '100', 254, 102, self.comp.RGB(255, 255, 255))
        self.speedNum = self.comp.TextLine(self.Board, '100 ms', 254, 136, self.comp.RGB(255, 255, 255))
        self.monsterNum = self.comp.TextLine(self.Board, '100', 254, 170, self.comp.RGB(255, 255, 255))
        self.RangeSlider = self.comp.SliderBar(self.Board, 0.0, self.Range_func, 73, 104)
        self.SpeedSlider = self.comp.SliderBar(self.Board, 0.0, self.Speed_func, 73, 137)
        self.MonsterSlider = self.comp.SliderBar(self.Board, 0.0, self.Monster_func, 73, 171)
        self.enableButton.SetOff()

        self.loadSettings()

        self.Speed_func()
        self.Range_func()
        self.Monster_func()
    
    def Monster_func(self):
        maxMonster = int(self.MonsterSlider.GetSliderPos()*1000)
        waithack_interface.SetMaxMonsters(maxMonster)
        self.monsterNum.SetText(str(self.maxMonster))
  
    def Range_func(self):
        range = int(self.RangeSlider.GetSliderPos()*10000)
        waithack_interface.SetRange(range)
        self.rangeNum.SetText(str(range))
    
    def Speed_func(self):
        speed = float(self.SpeedSlider.GetSliderPos())
        waithack_interface.SetSpeed(speed)
        self.speedNum.SetText(str(int(speed*1000)) + ' ms')

    def SwitchStart(self, val):
        if val:
            eXLib.BlockAttackPackets()
            waithack_interface.Start()
        else:
            eXLib.UnblockAttackPackets()
            waithack_interface.Stop()
    
    def OpenWindow(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

    def Close(self):
        self.Board.Hide()
        self.saveSettings()

Dmg = DmgHacksInstance()
Dmg.Show()