from BotBase import BotBase
from UIComponents import Component, TabWindow
import Movement
import chat, ui, chr, m2netm2g
import OpenLib
import eXLib


class Radar(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.all_vids = []
        self.showOre = True
        self.showMetins = True
        self.showPlayers = True
        self.showBoss = True

        self.metins = []
        self.ores = []
        self.players = []
        self.boss = []

        self.lastTime = 0
        self.lastTimeClearedList = 0
        self.BuildWindow()

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(290, 255)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Radar')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = Component()

        self.TabWidget = TabWindow(10, 30, 275, 220, self.Board,
                                                ['Setings', 'Ores', 'Metins', 'Players', 'Boss'])

        self.settings_tab = self.TabWidget.GetTab(0)
        self.ores_tab = self.TabWidget.GetTab(1)
        self.metins_tab = self.TabWidget.GetTab(2)
        self.players_tab = self.TabWidget.GetTab(3)
        self.boss_tab = self.TabWidget.GetTab(4)


        # Settings Tab
        self.enableButton = comp.OnOffButton(self.settings_tab, '', '', 15, 40,
                                             OffUpVisual='OpenBot/Images/start_0.tga',
                                             OffOverVisual='OpenBot/Images/start_1.tga',
                                             OffDownVisual='OpenBot/Images/start_2.tga',
                                             OnUpVisual='OpenBot/Images/stop_0.tga',
                                             OnOverVisual='OpenBot/Images/stop_1.tga',
                                             OnDownVisual='OpenBot/Images/stop_2.tga',
                                             funcState=self._start, defaultValue=False)

        self.showOreButton = comp.OnOffButton(self.settings_tab,
                                              '\t\t\t\t\t\tShow ore',
                                              '', 80, 40, funcState=self.switch_ore_button,
                                              defaultValue=self.showOre)

        self.showMetinsButton = comp.OnOffButton(self.settings_tab,
                                              '\t\t\t\t\t\tShow metins',
                                              '', 80, 55,  funcState=self.switch_metins_button,
                                              defaultValue=self.showMetins)
        self.showPlayersButton = comp.OnOffButton(self.settings_tab,
                                              '\t\t\t\t\t\tShow players',
                                              '', 80, 70, funcState=self.switch_player_button, defaultValue=self.showPlayers)

        self.showBossButton = comp.OnOffButton(self.settings_tab,
                                               '\t\t\t\t\t\tShow game masters', '', 80, 85,
                                               funcState=self.switch_boss_button,
                                               defaultValue=self.showBoss)


        x_size = 235
        y_size = 100
        # Ores Tab
        self.barOres, self.fileListBoxOres, self.ScrollBarOres = comp.ListBoxEx2(self.ores_tab, 10, 30, x_size, y_size)
        # Metins Tab
        self.barMetins, self.fileListBoxMetins, self.ScrollBarMetins = comp.ListBoxEx2(self.metins_tab, 10, 30, x_size, y_size)
        self.teleportToButtonMetin = comp.Button(self.metins_tab, 'Warp', '', 10, 150, self.warpToSelectedFileListBoxMetins,
                                            'd:/ymir work/ui/public/middle_button_01.sub',
                                            'd:/ymir work/ui/public/middle_button_02.sub',
                                            'd:/ymir work/ui/public/middle_button_03.sub')
        # Players Tab
        self.barPlayers, self.fileListBoxPlayers, self.ScrollBarPlayers = comp.ListBoxEx2(self.players_tab, 10, 30, x_size, y_size)
        self.teleportToButtonPlayer = comp.Button(self.players_tab, 'Warp', '', 10, 150, self.warpToSelectedFileListBoxPlayers,
                                            'd:/ymir work/ui/public/middle_button_01.sub',
                                            'd:/ymir work/ui/public/middle_button_02.sub',
                                            'd:/ymir work/ui/public/middle_button_03.sub')
        # Ores Tab
        self.barOres, self.fileListBoxOres, self.ScrollBarOres = comp.ListBoxEx2(self.ores_tab, 10, 30, x_size, y_size)
        self.teleportToButtonOres = comp.Button(self.ores_tab, 'Warp', '', 10, 150, self.warpToSelectedFileListBoxOres,
                                            'd:/ymir work/ui/public/middle_button_01.sub',
                                            'd:/ymir work/ui/public/middle_button_02.sub',
                                            'd:/ymir work/ui/public/middle_button_03.sub')
        # Boss Tab
        self.barBoss, self.fileListBoxBoss, self.ScrollBarBoss = comp.ListBoxEx2(self.boss_tab, 10, 30, x_size, y_size)
        self.teleportToButtonBoss = comp.Button(self.boss_tab, 'Warp', '', 10, 150, self.warpToSelectedFileListBoxBoss,
                                            'd:/ymir work/ui/public/middle_button_01.sub',
                                            'd:/ymir work/ui/public/middle_button_02.sub',
                                            'd:/ymir work/ui/public/middle_button_03.sub')

    def addToFileListBoxMetins(self, vid):
        x, y, z = chr.GetPixelPosition(vid)
        name = chr.GetNameByVID(vid)
        metin = {
            'vid': vid,
            'x': x,
            'y': y,
            'name': name
        }
        self.metins.append(metin)
        self.uptadeFileListBoxMetins()

    def uptadeFileListBoxMetins(self):
        self.fileListBoxMetins.RemoveAllItems()
        for metin in self.metins:
            self.fileListBoxMetins.AppendItem(OpenLib.Item(metin['name']))

    def warpToSelectedFileListBoxMetins(self):
        _item = self.fileListBoxMetins.GetSelectedItem()
        if _item is None:
            return
        metin_name = _item.GetText()
        for metin in self.metins:
            if metin['name'] == metin_name:
                Movement.TeleportToPosition(metin['x'], metin['y'])

    def addToFileListBoxPlayers(self, vid):
        x, y, z = chr.GetPixelPosition(vid)
        name = chr.GetNameByVID(vid)
        metin = {
            'vid': vid,
            'x': x,
            'y': y,
            'name': name
        }
        self.players.append(metin)
        self.uptadeFileListBoxPlayers()

    def uptadeFileListBoxPlayers(self):
        self.fileListBoxPlayers.RemoveAllItems()
        for player in self.players:
            self.fileListBoxPlayers.AppendItem(OpenLib.Item(player['name']))

    def warpToSelectedFileListBoxPlayers(self):
        _item = self.fileListBoxPlayers.GetSelectedItem()
        if _item is None:
            return
        player_name = _item.GetText()
        for player in self.players:
            if player['name'] == player_name:
                Movement.TeleportToPosition(player['x'], player['y'])

    def addToFileListBoxOres(self, vid):
        x, y, z = chr.GetPixelPosition(vid)
        name = chr.GetNameByVID(vid)
        ore = {
            'vid': vid,
            'x': x,
            'y': y,
            'name': name
        }
        self.ores.append(ore)
        self.uptadeFileListBoxOres()

    def uptadeFileListBoxOres(self):
        self.fileListBoxOres.RemoveAllItems()
        for ore in self.ores:
            self.fileListBoxOres.AppendItem(OpenLib.Item(ore['name']))

    def warpToSelectedFileListBoxOres(self):
        _item = self.fileListBoxBoss.GetSelectedItem()
        if _item is None:
            return
        boss_name = _item.GetText()
        for boss in self.boss:
            if boss['name'] == boss_name:
                Movement.TeleportToPosition(boss['x'], boss['y'])

    def addToFileListBoxBoss(self, vid):
        x, y, z = chr.GetPixelPosition(vid)
        name = chr.GetNameByVID(vid)
        boss = {
            'vid': vid,
            'x': x,
            'y': y,
            'name': name
        }
        self.boss.append(boss)
        self.uptadeFileListBoxBoss()

    def uptadeFileListBoxBoss(self):
        self.fileListBoxBoss.RemoveAllItems()
        for boss in self.boss:
            self.fileListBoxBoss.AppendItem(OpenLib.Item(boss['name']))

    def warpToSelectedFileListBoxBoss(self):
        _item = self.fileListBoxOres.GetSelectedItem()
        if _item is None:
            return
        ore_name = _item.GetText()
        for ore in self.ores:
            if ore['name'] == ore_name:
                Movement.TeleportToPosition(ore['x'], ore['y'])

    def switch_ore_button(self, val):
        self.showOre = val

    def switch_metins_button(self, val):
        self.showMetins = val

    def switch_player_button(self, val):
        self.showPlayers = val

    def switch_boss_button(self, val):
        self.showBoss = val

    def _start(self, val):
        if val:
            self.Start()
        else:
            self.Stop()

    def AddNewMetin(self, vid):
        self.addToFileListBoxMetins(vid)

    def IsThisMetinNew(self, vid):
        for metin in self.metins:
            if metin['vid'] == vid:
                return False
        return True

    def AddNewPlayer(self, vid):
        self.addToFileListBoxPlayers(vid)

    def IsThisPlayerNew(self, vid):
        for player in self.players:
            if player['vid'] == vid:
                return False
        return True

    def AddNewOre(self, vid):
        self.addToFileListBoxOres(vid)

    def IsThisBossNew(self, vid):
        for boss in self.boss:
            if boss['vid'] == vid:
                return False
        return True

    def AddNewBoss(self, vid):
        self.addToFileListBoxBoss(vid)

    def Frame(self):
        MAIN_CHAR_VID = m2netm2g.GetMainActorVID()

        self.all_vids = eXLib.InstancesList
        val, self.lastTimeClearedList = OpenLib.timeSleep(self.lastTimeClearedList, 5)
        if val:
            self.clear_lists()

        for vid in self.all_vids:
            if MAIN_CHAR_VID != vid:
                if self.showOre:
                    if OpenLib.IsThisOre(vid):
                        if self.IsThisOreNew(vid):
                            self.AddNewOre(vid)
                if self.showMetins:
                    if OpenLib.IsThisMetin(vid):
                        if self.IsThisMetinNew(vid):
                            self.AddNewMetin(vid)
                if self.showPlayers:
                    if OpenLib.IsThisPlayer(vid):
                        if self.IsThisPlayerNew(vid):
                            self.AddNewPlayer(vid)
                if self.showBoss:
                    if OpenLib.IsThisBoss(vid):
                        if self.IsThisBossNew(vid):
                            self.AddNewBoss(vid)

    def clear_lists(self):
        self.fileListBoxOres.RemoveAllItems()
        self.ores = []
        self.fileListBoxMetins.RemoveAllItems()
        self.metins = []
        self.fileListBoxPlayers.RemoveAllItems()
        self.players = []

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

def switch_state():
    radar.switch_state()

radar = Radar()