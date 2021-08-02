from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Settings import ItemListDialog
from OpenBot.Modules.Actions import ActionFunctions, ActionRequirementsCheckers, ActionBot
from BotBase import BotBase
import UIComponents, OpenLib
import ui, player, background, chat, item

#
#DT Blacksmith 20074
#DT Weapon Blacksmith 20075
#DT Jewelry Blacksmith 20076
#Demontower 20348
# METIN POS 14080 64335

"""
,
        7: { # stage with metins and chests
            'actions': [{ 'args': [(61017, 66483)],
                          'function': ActionFunctions.FindMapInDT,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (60961, 42600, 25000)},
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }
                
            ],},
        8: { # stage with key
            'actions': [
                { 'args': [(60961, 42600)],
                          'function': ActionFunctions.OpenASealInMonument,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (61127, 17160, 25000)},
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }
                        ],},
        9: { # stage with ripper
            'actions': [{ 'args': [(61127, 17160)],
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {}, # DONT NEED ANY
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }

                        ],},

"""

# DUNGEON SCHEMA
DEAMON_TOWER = {
    'requirements': {
        'maps': ['metin2_map_milgyo', 'metin2_map_deviltower1'],
        'lvl': 40,},
    'options': {
        'shouldUpgradeItem': False,
        'GoAboveBlacksmith': False,},
    'stages': {
        0: { # stage outside devil tower, entering dt
            'actions': [{ 'args': [20348, (53200, 59600), [0, 0], 'metin2_map_milgyo'], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.TalkWithNPC,
                          'on_success': [ActionBot.NEXT_ACTION],
                          'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: (19004, 69011, 20000)}}]

            },
        1: { # stage with metin
            'actions': [{'args': [(19004, 69011)], # position
                        'function': ActionFunctions.MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (19004, 69011)}
                        },
                        {'args': [8015],
                        'function': ActionFunctions.Find,
                        'requirements': {},
                        'on_success': [ActionBot.NEXT_ACTION],
                        'on_failed': []
                        },
                        {'args': [8015, 0],
                        'function': ActionFunctions.Destroy,
                        'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (12599, 38399, 1000)},
                        'on_success': [ActionBot.NEXT_ACTION],
                        'on_failed': []
                        }]},
        2: { # stage with only deamons
            'actions': [{ 'args': [(15003, 40961)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (13400, 14700, 1000)}, #
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }],},
        3: { # stage with king
            'actions': [{ 'args': [(17688, 19619)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (37037, 62659, 2000)}, # 
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }],},
        4: { # stage with metins
            'actions': [{ 'args': [(39123, 65131)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (39539, 43607, 5000)}, # IS_NEAR_POSITION: (37722, 63632, 1000)
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }],},
        5: { # stage with keys
            'actions': [{ 'args': [(40000, 44000)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.OpenAllSeals,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (40713, 19914, 5000)},
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }],},
        6: { # stage with blacksmith
            'actions': [{ 'args': [(41000, 20000)],
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {},
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }

                        ],}

    }
}


class AutoDungeon(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.currSchema = None
        self.currStage = 0
        self.currAction = 0
        self.isCurrActionDone = True
        self.itemFilterList = None
        self.itemToUpgrade = []

        self.options = {
            'UseDmgHack': False,
            'NextChannelIfThereIsAnotherPlayer': False
        }

        self.BuildWindow()

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 235)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Auto Dungeon')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        comp = UIComponents.Component()

        self.TabWidget = UIComponents.TabWindow(10, 30, 215, 195, self.Board, ['DT', 'Settings'])
        
        self.deamon_tower_tab = self.TabWidget.GetTab(0)
        self.settings_tab = self.TabWidget.GetTab(1)

        
        self.shouldUpgradeItemButton = comp.OnOffButton(self.deamon_tower_tab, '\t\t\t\t\t\t Upgrade item?', 'If u want upgrade item on blacksmith stage, check this', 10, 20,
                                                      funcState=self.switch_should_upgrade_item,
                                                      defaultValue=DEAMON_TOWER['options']['shouldUpgradeItem'])      




        #self.slotBarSlotToUpgrade, self.edit_lineWaitingTime = comp.EditLine(self.deamon_tower_tab, '0', 20, 20, 25, 15, 25)             
        #self.text_line1 = comp.TextLine(self.deamon_tower_tab, 'slot with item to ugprade', 50, 20, comp.RGB(255, 255, 255))
        #
        # self.text_line2 = comp.TextLine(self.deamon_tower_tab, 'set -1 to disable', 65, 30, comp.RGB(255, 255, 255))
        
        self.goAboveBlacksmithButton = comp.OnOffButton(self.deamon_tower_tab, '\t\t\t\t\t\tGo above blacksmith?', 'Check if u want kill ripper', 10, 50,
                                                      funcState=self.switch_go_above_blacksmith_button,
                                                      defaultValue=DEAMON_TOWER['options']['GoAboveBlacksmith'])
        
        self.barItems, self.fileListBox, self.ScrollBar = comp.ListBoxEx2(self.deamon_tower_tab, 10, 75, 130, 75)
       
        self.openItemFilterButton = comp.Button(self.deamon_tower_tab, 'Open item list', '', 110, 20, self.open_item_filter_dialog,
                                        'd:/ymir work/ui/public/large_Button_01.sub',
                                        'd:/ymir work/ui/public/large_Button_02.sub',
                                        'd:/ymir work/ui/public/large_Button_03.sub')
        
        self.deleteSelectedItemButton = comp.Button(self.deamon_tower_tab, 'Delete', '', 165, 60, self.DeleteItemFilterList,
                                        'd:/ymir work/ui/public/small_Button_01.sub',
                                        'd:/ymir work/ui/public/small_Button_02.sub',
                                        'd:/ymir work/ui/public/small_Button_03.sub')
        
        self.clearListBox = comp.Button(self.deamon_tower_tab, 'Clear', '', 165, 85, self.ClearFilterList,
                                        'd:/ymir work/ui/public/small_Button_01.sub',
                                        'd:/ymir work/ui/public/small_Button_02.sub',
                                        'd:/ymir work/ui/public/small_Button_03.sub')

        self.enableDeamonTower = comp.OnOffButton(self.deamon_tower_tab, '', '', 165, 110,
                                                    OffUpVisual='OpenBot/Images/start_0.tga',
                                                    OffOverVisual='OpenBot/Images/start_1.tga',
                                                    OffDownVisual='OpenBot/Images/start_2.tga',
                                                    OnUpVisual='OpenBot/Images/stop_0.tga',
                                                    OnOverVisual='OpenBot/Images/stop_1.tga',
                                                    OnDownVisual='OpenBot/Images/stop_2.tga',
                                                    funcState=self.switch_launch_auto_dungeon, defaultValue=False)

        self.showNextChannelIfThereIsAnotherPlayerButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tAvoid players', '', 20, 50, funcState=self.switch_next_channel_if_there_is_another_player, defaultValue=self.options['NextChannelIfThereIsAnotherPlayer'])

    def switch_is_curr_action_done(self):
        if self.isCurrActionDone:
            self.isCurrActionDone = False
        else:
            self.GoToNextAction()
            self.isCurrActionDone = True

    def switch_should_upgrade_item(self, val):
        DEAMON_TOWER['options']['shouldUpgradeItem'] = val
        if val:
            if self.itemFilterList == None:
                self.itemFilterList = ItemListDialog(self.addPickFilterItem, 290, 40)
        else:
            self.itemFilterList = None

    def open_item_filter_dialog(self):
        if self.itemFilterList == None:
            self.itemFilterList = ItemListDialog(self.addPickFilterItem, 290, 40)

    def ClearFilterList(self):
        self.itemToUpgrade = []
        self.fileListBox.RemoveAllItems()
        self.UpdateFilterList()

    def UpdateFilterList(self):	
        self.fileListBox.RemoveAllItems()
        for filterItem in sorted(self.itemToUpgrade):
            item.SelectItem(filterItem)
            name = item.GetItemName()
            self.fileListBox.AppendItem(OpenLib.Item(str(filterItem)+" "+name))
                
    def DeleteItemFilterList(self):
        _item = self.fileListBox.GetSelectedItem()
        if _item == None:
            return
        item_name = _item.GetText()
        id = item_name.split(" ",1)
        self.itemToUpgrade.remove(int(id[0]))
        self.UpdateFilterList()

    
    def addPickFilterItem(self,id):
        self.itemToUpgrade.append(int(id))
        self.UpdateFilterList()

    def switch_go_above_blacksmith_button(self, val):
        DEAMON_TOWER['options']['GoAboveBlacksmith'] = val

    def switch_next_channel_if_there_is_another_player(self, val):
        self.options['NextChannelIfThereIsAnotherPlayer'] = val

    def switch_launch_auto_dungeon(self, val):
        if val:
            self.StartDeamonTower()
        else:
            self.Stop()

    def StartDeamonTower(self):
        self.currSchema = DEAMON_TOWER
        #text = self.edit_lineWaitingTime.GetText()
        #if self.is_text_validate(text):
        #    self.currSchema['options']['SlotToUpgrade'] = int(text)
        #else:
        #    return

        self.AddOptionalActionsToDeamonTower()
        if self.CheckRequirementsForCurrSchema():

            if str(background.GetCurrentMapName()) == 'metin2_map_deviltower1':
                if ActionRequirementsCheckers.isNearPosition((15800, 64400, 10000)):
                    self.currStage = 1
                elif ActionRequirementsCheckers.isNearPosition((12599, 38399, 10000)):
                    self.currStage = 2
                elif ActionRequirementsCheckers.isNearPosition((18000, 18000, 10000)):
                    self.currStage = 3
                elif ActionRequirementsCheckers.isNearPosition((37037, 62659, 10000)):
                    self.currStage = 4
                elif ActionRequirementsCheckers.isNearPosition((39539, 43607, 10000)):
                    self.currStage = 5
                elif ActionRequirementsCheckers.isNearPosition((40713, 19914, 10000)):
                    self.currStage = 6
                elif ActionRequirementsCheckers.isNearPosition((61017, 66483, 25000)):
                    self.currStage = 7
                elif ActionRequirementsCheckers.isNearPosition((60961, 42631, 25000)):
                    self.currStage = 8
                elif ActionRequirementsCheckers.isNearPosition((61127, 17162, 25000)):
                    self.currStage = 9
                else:
                    DebugPrint('Invalid stage')
                    return
            else:
                self.currStage = 0

            self.Start()
        else:
            self.currSchema = None            

    def AddOptionalActionsToDeamonTower(self):
        slot_to_upgrade = -1
        if self.currSchema['options']['shouldUpgradeItem']:
            for item in self.itemToUpgrade:
                slot = OpenLib.GetItemByID(item)
                if slot > -1:
                    slot_to_upgrade = slot
                    break

        action_dict = {
            'args': [self.currSchema['options']['GoAboveBlacksmith'], slot_to_upgrade],
            'function': ActionFunctions.LookForBlacksmithInDeamonTower,
            'requirements':  {},
            'on_failed': [ActionBot.DISCARD]
        }
        self.currSchema['stages'][6]['actions'].append(action_dict)
        DebugPrint(str(self.currSchema))



    def Frame(self):
        if self.isCurrActionDone:
            action_dict = self.currSchema['stages'][self.currStage]['actions'][self.currAction]
            action_dict['callback'] = self.SetIsCurrActionDoneTrue
            self.isCurrActionDone = False
            ActionBot.instance.AddNewAction(action_dict)
            DebugPrint(str(action_dict))

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

    def is_text_validate(self, text):
        try:
            int(text)
        except ValueError:
            chat.AppendChat(3, '[Farmbot] - The value must be a digit')
            return False
        if int(text) < -2:
            chat.AppendChat(3, '[Farmbot] - The value must be in range -1 to infinity')
            return False
        return True


def switch_state():
    global instance
    instance.switch_state()

instance = AutoDungeon()