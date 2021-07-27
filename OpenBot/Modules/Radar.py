from BotBase import BotBase
from UIComponents import Component, TabWindow
import Movement
import chat, ui, chr, m2netm2g, background
import OpenLib
import eXLib
import re


class Radar(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.all_vids = []
        self.showOre = True
        self.showMetins = True
        self.showPlayers = True
        self.showBoss = True

        self.entities = []

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

        self.TabWidget = TabWindow(10, 30, 275, 220, self.Board, ['Settings', 'Entities'])

        self.settings_tab = self.TabWidget.GetTab(0)
        self.entities_list = self.TabWidget.GetTab(1)



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
                                              '', 80, 60,  funcState=self.switch_metins_button,
                                              defaultValue=self.showMetins)
        self.showPlayersButton = comp.OnOffButton(self.settings_tab,
                                              '\t\t\t\t\t\tShow players',
                                              '', 80, 80, funcState=self.switch_player_button, defaultValue=self.showPlayers)

        self.showBossButton = comp.OnOffButton(self.settings_tab,
                                               '\t\t\t\t\t\tShow boss', '', 80, 100,
                                               funcState=self.switch_boss_button,
                                               defaultValue=self.showBoss)


        x_size = 235
        y_size = 100

        # Metins Tab
        self.barEntities, self.fileListBoxEntities, self.ScrollBarEntities = comp.ListBoxEx2(self.entities_list, 10,
                                                                                             30, x_size, y_size)
        self.teleportButton = comp.Button(self.entities_list, 'Warp', '', 10, 150, self.warpToSelectedFileListBoxEntities,
                                          'd:/ymir work/ui/public/middle_button_01.sub',
                                          'd:/ymir work/ui/public/middle_button_02.sub',
                                          'd:/ymir work/ui/public/middle_button_03.sub')

    def addToFileListBoxEntities(self, vid, instance_type=OpenLib.NONE_TYPE):
        x, y, z = chr.GetPixelPosition(vid)
        name = chr.GetNameByVID(vid)
        entity = {
            'type': instance_type,
            'vid': vid,
            'x': x,
            'y': y,
            'name': name
        }
        self.entities.append(entity)
        self.updateFileListBoxEntities()

    def getTypeName(self, instance_type):
        if instance_type == OpenLib.NONE_TYPE:
            return '[ NONE ] '
        elif instance_type == OpenLib.ORE_TYPE:
            return '[ ORE ] '
        elif instance_type == OpenLib.METIN_TYPE:
            return '[ METIN ] '
        elif instance_type == OpenLib.BOSS_TYPE:
            return '[ BOSS ] '
        elif instance_type == OpenLib.PLAYER_TYPE:
            return '[ PLAYER ] '

    def updateFileListBoxEntities(self):
        self.fileListBoxEntities.RemoveAllItems()
        for entity in self.entities:
            if not entity['name'] == 'None':
                self.fileListBoxEntities.AppendItem(OpenLib.Item(self.getTypeName(entity['type']) + entity['name']))

    def warpToSelectedFileListBoxEntities(self):
        _item = self.fileListBoxEntities.GetSelectedItem()
        if _item is None:
            return
        item_text = _item.GetText()
        type_words_patterns = '[ [A-Z]+ ] '
        type = re.findall(type_words_patterns, item_text)
        name = item_text.split(type[0])

        for entity in self.entities:
            if entity['name'] == str(name[1]):
                Movement.TeleportToPosition(entity['x'], entity['y'])

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

    def AddNewEntity(self, vid, instance_type=OpenLib.NONE_TYPE):
        self.addToFileListBoxEntities(vid, instance_type=instance_type)

    def IsThisEntityNew(self, vid):
        for entity in self.entities:
            if entity['vid'] == vid:
                return False
        return True

    def Frame(self):
        MAIN_CHAR_VID = m2netm2g.GetMainActorVID()
        
        self.all_vids = eXLib.InstancesList
        val, self.lastTimeClearedList = OpenLib.timeSleep(self.lastTimeClearedList, 5)
        if val:
            self.clear_lists()

        for vid in self.all_vids:
            if MAIN_CHAR_VID != vid:
                chr.SelectInstance(vid)
                chat.AppendChat(3, str(chr.GetInstanceType(vid)) + ' ' + str(chr.GetRace()) + ' ' + str(chr.GetName(vid)) + ' ' + str(chr.GetPixelPosition(vid))   + ' ' + str(vid) )

                if self.IsThisEntityNew(vid):
                    if self.showOre:
                        if OpenLib.IsThisOre(vid):
                            self.AddNewEntity(vid, OpenLib.ORE_TYPE)
                    if self.showMetins:
                        if OpenLib.IsThisMetin(vid):
                            self.AddNewEntity(vid, OpenLib.METIN_TYPE)
                    if self.showPlayers:
                        if OpenLib.IsThisPlayer(vid):
                            self.AddNewEntity(vid, OpenLib.PLAYER_TYPE)
                    if self.showBoss:
                        if OpenLib.IsThisBoss(vid):
                            self.AddNewEntity(vid, OpenLib.BOSS_TYPE)

    def clear_lists(self):
        self.fileListBoxEntities.RemoveAllItems()
        self.entities = []

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

def switch_state():
    radar.switch_state()

radar = Radar()