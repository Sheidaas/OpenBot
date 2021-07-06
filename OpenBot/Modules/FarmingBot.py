from BotBase import BotBase
import DmgHacks
import Movement
import OpenLib
import UIComponents
import player, ui, chat, chr, net
import eXLib

# STATES
WALKING_STATE = 1
MINING_STATE = 2
FARMING_STATE = 3


class FarmingBot(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.CURRENT_STATE = WALKING_STATE
        self.is_walking = True  # if False character is using teleport, otherwise character is walking
        self.current_point = 0  # Current position index
        self.path = []  # Dict of tuples with coordinates [(0, 0), (2, 2)] etc

        self.lastTime = 0

        self.farm_metins = True
        self.metins_vid_list = []
        self.selectedMetin = 0
        self.farm_ores = False
        self.ores_vid_list = []
        self.selectedOre = 0


        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(240, 300)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('FarmBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = UIComponents.Component()
        self.TabWidget = UIComponents.TabWindow(10, 30, 220, 260, self.Board,
                                                ['Moving', 'Mining', 'Metins'])
        self.moving_tab = self.TabWidget.GetTab(0)
        self.minings_tab = self.TabWidget.GetTab(1)
        self.metins_tab = self.TabWidget.GetTab(2)

        self.barItems, self.fileListBox, self.ScrollBar = comp.ListBoxEx2(self.moving_tab, 10, 30, 180, 100)
        self.addPointButton = comp.Button(self.moving_tab, 'Add', '', 10, 150, self.add_point,
                                          'd:/ymir work/ui/public/small_Button_01.sub',
                                          'd:/ymir work/ui/public/small_Button_02.sub',
                                          'd:/ymir work/ui/public/small_Button_03.sub')
        self.deletePointButton = comp.Button(self.moving_tab, 'Delete', '', 10, 170, self.remove_selected,
                                             'd:/ymir work/ui/public/small_Button_01.sub',
                                             'd:/ymir work/ui/public/small_Button_02.sub',
                                             'd:/ymir work/ui/public/small_Button_03.sub')
        self.enableButton = comp.OnOffButton(self.moving_tab, '', '', 70, 150,
                                             OffUpVisual='OpenBot/Images/start_0.tga',
                                             OffOverVisual='OpenBot/Images/start_1.tga',
                                             OffDownVisual='OpenBot/Images/start_2.tga',
                                             OnUpVisual='OpenBot/Images/stop_0.tga',
                                             OnOverVisual='OpenBot/Images/stop_1.tga',
                                             OnDownVisual='OpenBot/Images/stop_2.tga',
                                             funcState=self._start, defaultValue=False)

        self.showWalkButton = comp.OnOffButton(self.moving_tab,
                                              '\t\t\t\t\t\tWalk?',
                                              '', 125, 150,  funcState=self.switch_walking,
                                              defaultValue=self.is_walking)
        self.showMiningButton = comp.OnOffButton(self.moving_tab,
                                              '\t\t\t\t\t\tMining?',
                                              '', 125, 170, funcState=self.switch_mining, defaultValue=self.farm_ores)

        self.showFarmingMetinButton = comp.OnOffButton(self.moving_tab,
                                              '\t\t\t\t\t\tMetins?',
                                              '', 125, 190, funcState=self.switch_farming_metin,
                                                 defaultValue=self.farm_metins)

    def switch_walking(self, val):
        self.is_walking = val

    def switch_mining(self, val):
        self.farm_ores = val

    def switch_farming_metin(self, val):
        self.farm_metins = val

    def add_point(self):
        (x, y, z) = player.GetMainCharacterPosition()
        self.path.append((x, y))
        self.update_points_list()

    def remove_selected(self):
        _item = self.fileListBox.GetSelectedItem()
        if _item is None:
            return
        _item_text = _item.GetText().split(':')
        position = (float(_item_text[0]), float(_item_text[1]))
        self.path.remove(position)
        self.update_points_list()

    def update_points_list(self):
        self.fileListBox.RemoveAllItems()
        for position in self.path:
            self.fileListBox.AppendItem(OpenLib.Item(str(position[0]) + ':' + str(position[1])))

    def next_point(self):
        self.is_waypoint_reached = True
        if self.current_point + 1 >= len(self.path):
            self.path.reverse()
            self.current_point = 1
        else:
            self.current_point += 1

    def go_to_next_position(self):
        self.Move(self.path[self.current_point][0], self.path[self.current_point][1], callback=self.onWaypointReach)

    def select_metin(self):
        if(len(self.metins_vid_list) > 0):
            self.selectedMetin = self.metins_vid_list.pop()
            chat.AppendChat(3,str(self.selectedMetin))
    def select_ore(self):
        if(len(self.ores_vid_list) > 0):
            self.selectedOre = self.ores_vid_list.pop()

    def onWaypointReach(self):
        self.next_point()
        self.CURRENT_STATE = WALKING_STATE

    def _start(self, val):
        if not val:
            self.Stop()
        else:
            self.Start()

    def StartBot(self):
        if len(self.path) < 2:
            self.Stop()
            return

    def StopBot(self):
        self.current_point = 0
        Movement.StopMovement()
        self.CURRENT_STATE = WALKING_STATE

    def Move(self, x, y, callback=None):
        if self.is_walking:
            if callback is None:
                Movement.GoToPositionAvoidingObjects(x, y)
            else:
                Movement.GoToPositionAvoidingObjects(x, y, callback=callback)
        else:
            Movement.TeleportToPosition(x, y)
            if callback is not None:
                callback()

    def MoveToVid(self, vid, callback=None):
        chr.SelectInstance(vid)
        x, y, z = chr.GetPixelPosition(vid)
        self.Move(x, y, callback)

    def Frame(self):
        if self.CURRENT_STATE == WALKING_STATE:
            self.ores_vid_list = []
            self.metins_vid_list = []
            self.checkForMetinsAndOres()

            if self.farm_metins and len(self.metins_vid_list)>0:
                self.select_metin()
                self.CURRENT_STATE = FARMING_STATE
            
            elif self.farm_ores and len(self.metins_vid_list)>0:
                self.select_ore()
                self.CURRENT_STATE = MINING_STATE
            else:
                self.go_to_next_position()
                
            return
        elif self.CURRENT_STATE == MINING_STATE:
            pass
        elif self.CURRENT_STATE == FARMING_STATE:
            self.farmMetin()

    def mineOre(self):
        self.is_mining = True

        # Checking there is any reason to stop mining
        if not self.is_char_ready_to_mine():
            self.Stop()
            return
        OpenLib.RotateMainCharacterByVid(self.current_mining_ore)
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 12)
        if val:
            self.lastTime = OpenLib.GetTime()
            net.SendOnClickPacket(self.current_mining_ore)

    def farmMetin(self):

        vid_life_status = OpenLib.AttackTarget(self.selectedMetin)

        if vid_life_status == -1:
            player.SetAttackKeyState(False)
            DmgHacks.Pause()
            self.selectedMetin = 0
            self.CURRENT_STATE = WALKING_STATE

        elif vid_life_status == 0:
            DmgHacks.Resume()

        elif vid_life_status == 1:
            DmgHacks.Resume()

    def checkForMetinsAndOres(self):
        for vid in eXLib.InstancesList:
            if OpenLib.IsThisOre(vid):
                self.ores_vid_list.append(vid)
            elif OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
                self.metins_vid_list.append(vid)

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

    def is_char_ready_to_mine(self):
        if OpenLib.isPlayerCloseToInstance(self.current_mining_ore):
            return False
        return True


def switch_state():
    farm.switch_state()


farm = FarmingBot()