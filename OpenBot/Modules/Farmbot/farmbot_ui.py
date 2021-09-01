from OpenBot.Modules import OpenLib, Hooks, UIComponents
from OpenBot.Modules.BotBase import BotBase
from OpenBot.Modules.Actions import ActionBot
from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
import player, ui, chat, chr, net, background


def __PhaseTurnOnFarmbot(phase):
    global farm
    if phase == OpenLib.PHASE_GAME:
        if farmbot_ui.enableButton.isOn:
            farmbot_interface.Start()


class FarmingBotUI(BotBase):

    def __init__(self):
        self.BuildWindow()


    def BuildWindow(self):
        status = farmbot_interface.GetStatus()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(240, 300)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('FarmBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = UIComponents.Component()
        self.TabWidget = UIComponents.TabWindow(10, 30, 220, 260, self.Board,
                                                ['Moving', 'Mining', 'Settings'])
        self.moving_tab = self.TabWidget.GetTab(0)
        self.minings_tab = self.TabWidget.GetTab(1)
        self.settings_tab = self.TabWidget.GetTab(2)

        # Moving tab
        self.barItems, self.fileListBox, self.ScrollBar = comp.ListBoxEx2(self.moving_tab, 10, 30, 180, 100)
        self.addPointButton = comp.Button(self.moving_tab, 'Add', 'Add current position to path', 10, 140, self.add_point,
                                          'd:/ymir work/ui/public/small_Button_01.sub',
                                          'd:/ymir work/ui/public/small_Button_02.sub',
                                          'd:/ymir work/ui/public/small_Button_03.sub')

        self.deletePointButton = comp.Button(self.moving_tab, 'Delete', 'Delete selected position in path', 10, 165, self.remove_selected,
                                             'd:/ymir work/ui/public/small_Button_01.sub',
                                             'd:/ymir work/ui/public/small_Button_02.sub',
                                             'd:/ymir work/ui/public/small_Button_03.sub')
        self.deleteAllPointsButton = comp.Button(self.moving_tab, 'Clear', 'Clear path', 10, 190, self.remove_all,
                                             'd:/ymir work/ui/public/small_Button_01.sub',
                                             'd:/ymir work/ui/public/small_Button_02.sub',
                                             'd:/ymir work/ui/public/small_Button_03.sub')

        self.enableButton = comp.OnOffButton(self.moving_tab, '', 'Start', 70, 140,
                                             OffUpVisual='OpenBot/Images/start_0.tga',
                                             OffOverVisual='OpenBot/Images/start_1.tga',
                                             OffDownVisual='OpenBot/Images/start_2.tga',
                                             OnUpVisual='OpenBot/Images/stop_0.tga',
                                             OnOverVisual='OpenBot/Images/stop_1.tga',
                                             OnDownVisual='OpenBot/Images/stop_2.tga',
                                             funcState=self.OnEnableSwitchButton, defaultValue=status['Enabled'])

        self.showMiningButton = comp.OnOffButton(self.moving_tab, '\t\t\t\t\t\tMining?',
        'Do you want to mine?', 125, 140, funcState=farmbot_interface.SwitchLookForOre, defaultValue=status['LookForOre'])

        self.showFarmingMetinButton = comp.OnOffButton(self.moving_tab, '\t\t\t\t\t\tMetins?',
        'Do you want farm metins?', 125, 160, funcState=farmbot_interface.SwitchLookForMetins, defaultValue=status['LookForMetins'])

        # Ores tab
        index_y = 0
        index_x = 0
        for ore in OpenLib.ORES_IDS:
            setattr(self, 'is_mine_' + str(ore), False)
            button = comp.OnOffButton(self.minings_tab, '', '', 30+(index_x*60), 30+(index_y*40),
                                      image="icon/item/"+OpenLib.ORES_IDS[ore]+".tga",
                                      funcState=self.create_switch_function(ore),
                                      defaultValue=False)
            setattr(self, str(ore)+'Button', button)

            index_y += 1
            if index_y % 4 == 0:
                index_y = 0
                index_x += 1

        # Settings tab
        self.settingsLoadButton =   comp.Button(self.settings_tab, 'Load', 'Load path by name of file', 20, 30, self.load_path,
                                             'd:/ymir work/ui/public/small_Button_01.sub',
                                             'd:/ymir work/ui/public/small_Button_02.sub',
                                             'd:/ymir work/ui/public/small_Button_03.sub')

        self.text_lineEditLine = comp.TextLine(self.settings_tab, 'name of file to load/save', 75, 20, comp.RGB(255, 255, 255))
        self.slot_bar, self.edit_line = comp.EditLine(self.settings_tab, 'filename.txt', 70, 40, 120, 25, 25)

        self.settingsSaveButton =   comp.Button(self.settings_tab, 'Save', 'Save path by name of file', 20, 55, self.save_path,
                                             'd:/ymir work/ui/public/small_Button_01.sub',
                                             'd:/ymir work/ui/public/small_Button_02.sub',
                                             'd:/ymir work/ui/public/small_Button_03.sub')



        self.showChannelSwitchingButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\tSwitch channels',
         'If checked, farmbot will change to next channel after complete a path', 20, 80,
                                                      funcState=farmbot_interface.SwitchChangeChannel,
                                                      defaultValue=status['ChangeChannel'])

                
        self.showAlwaysWaithackButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\t\tAlways use waithack', 'If check, waithack will be turned on even while walking', 20, 100,
                                                         funcState=self.switch_always_use_waithack,
                                                         defaultValue=ActionBot.instance.showAlwaysWaithackButton)

        self.showOffWaithackButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tDont use waithack', 'If checked, farmbot wont use waithack for destroying metin', 20, 120,
                                                      funcState=self.switch_dont_use_waithack,
                                                      defaultValue=ActionBot.instance.showOffWaithackButton)

        self.showExchangeTrash = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\t\t\t\t\t\t\tExchange to energy fragments', 'This option allow farmbot to exchange items listed in settings > shop to energy fragments.', 20, 140,
                                                funcState=farmbot_interface.SwitchExchangeItemsToEnergy,
                                                defaultValue=status['ExchangeItemsToEnergy'])                                                 

        self.slot_barWaitingTime, self.edit_lineWaitingTime = \
            comp.EditLine(self.settings_tab, str(status['WaitingTime']), 20, 170, 40, 20, 25)

        self.text_lineWaitingTime = comp.TextLine(self.settings_tab, 's. of waiting after ', 70, 175, comp.RGB(255, 255, 255))
        self.text_lineWaitingTime1 = comp.TextLine(self.settings_tab, 'destorying metin',  75, 185, comp.RGB(255, 255, 255))

    def load_path(self):
        filename = self.edit_line.GetText()
        if farmbot_interface.LoadPath(filename):
            self.update_points_list()
            chat.AppendChat(3, '[Farmbot] - Successfully load ' + filename)

        else:
            chat.AppendChat(3, '[Farmbot] - Cannot load ' + filename)

    def save_path(self):
        filename = self.edit_line.GetText()
        if farmbot_interface.SavePath(filename):
            chat.AppendChat(3, '[Farmbot] - Successfully saved ' + filename)
        else:
            chat.AppendChat(3, '[Farmbot] - Cannot save ' + filename)

    def switch_always_use_waithack(self, val):
        ActionBot.instance.showAlwaysWaithackButton = val

    def switch_dont_use_waithack(self, val):
        ActionBot.instance.showOffWaithackButton = val

    def OnEnableSwitchButton(self, val):
        if val:
            result = farmbot_interface.Start()
            if not result:
                self.enableButton.SetOff()
        else:
            farmbot_interface.Stop()

    def ButtonOnOff(self, val):
        pass

    def remove_all(self):
        self.fileListBox.RemoveAllItems()
        farmbot_interface.ClearPath()

    def switch_func(self, val):
        pass


    def create_switch_function(self, ore_id):

        def function(val):
            if val:
                farmbot_interface.AddOreToMine(ore_id)
            else:
                farmbot_interface.RemoveOreToMine(ore_id)

        return function

    def add_point(self):
        x, y, z = player.GetMainCharacterPosition()
        point = {'x': x, 'y': y, 'map_name': background.GetCurrentMapName()}
        if farmbot_interface.AddPoint(point):
            self.update_points_list()
        else:
            chat.AppendChat(3, '[Farmbot] - Cannot add point to path')

    def remove_selected(self):
        _item = self.fileListBox.GetSelectedItem()
        if _item is None:
            return
        _item_text = _item.GetText().split(':')
        point = {'x': float(_item_text[0]), 'y': float(_item_text[1]), 'map_name': str(_item_text[2])}
        if farmbot_interface.RemovePoint(point):
            self.update_points_list()
        else:
            chat.AppendChat(3, '[Farmbot] - Cannot remove point from path')

    def update_points_list(self):
        self.fileListBox.RemoveAllItems()
        for position in farmbot_interface.GetStatus()['Path']:
            x, y = int(position[0]), int(position[1])
            self.fileListBox.AppendItem(OpenLib.Item(str(x) + ':' + str(y) + ':' + position[2]))

    def is_text_validate(self, text):
        try:
            int(text)
        except ValueError:
            chat.AppendChat(3, '[Farmbot] - The value must be a digit')
            return False
        if int(text) < 0:
            chat.AppendChat(3, '[Farmbot] - The value must be in range 0 to infinity')
            return False
        return True

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

farmbot_ui = FarmingBotUI()
Hooks.registerPhaseCallback('farmbotCallback', __PhaseTurnOnFarmbot)