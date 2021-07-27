from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Actions import ActionFunctions, ActionRequirementsCheckers, ActionBot
from BotBase import BotBase
import UIComponents, OpenLog
import ui, player, background, chat

#
#DT Blacksmith 20074
#DT Weapon Blacksmith 20075
#DT Jewelry Blacksmith 20076
#Demontower 20348
# METIN POS 14080 64335

# DUNGEON SCHEMA
DEAMON_TOWER = {
    'requirements': {
        'maps': ['metin2_map_milgyo', 'metin2_map_deviltower1'],
        'lvl': 40,},
    'options': {
        'UseBlacksmith': False,
        'SlotToUpgrade': 0,
        'GoAboveBlacksmith': False,},
    'stages': {
        0: { # stage outside devil tower, entering dt
            'actions': [{ 'args': [20348, (53200, 59600), [0, 0]], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.TalkWithNPC,
                          'requirements': { ActionRequirementsCheckers.IS_IN_MAP: ['metin2_map_deviltower1'] }

            }]},
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
                          'on_failed': [ActionBot.NEXT_ACTION]
                        }],},
        3: { # stage with king
            'actions': [{ 'args': [(17688, 19619)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (37037, 62659, 2000)}, # 
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': [ActionBot.NEXT_ACTION]
                        }],},
        4: { # stage with metins
            'actions': [{ 'args': [(39123, 65131)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (39539, 43607, 5000)}, # IS_NEAR_POSITION: (37722, 63632, 1000)
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': [ActionBot.NEXT_ACTION]
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

                        ],},},
        7: { # stage with metins and chests
            'actions': [{ 'args': [(61500, 20000)],
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {}, # DONT NEED ANY
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }

                        ],},
        8: { # stage with keys
            'actions': [{ 'args': [(61690, 42200)],
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (40713, 19914, 5000)}, # DONT NEED ANY
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }

                        ],},
        9: { # stage with ripper
            'actions': [{ 'args': [(61690, 61690)],
                          'function': ActionFunctions.ClearFloor,
                          'requirements': {}, # DONT NEED ANY
                          'on_success': [ActionBot.NEXT_ACTION],
                          'on_failed': []
                        }

                        ],},
        }


class AutoDungeon(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.currSchema = None
        self.currStage = 0
        self.currAction = 0
        self.isCurrActionDone = True

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
                                
        self.enableDeamonTower = comp.OnOffButton(self.deamon_tower_tab, '', '', 150, 110,
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



    def switch_next_channel_if_there_is_another_player(self, val):
        self.options['NextChannelIfThereIsAnotherPlayer'] = val

    def switch_launch_auto_dungeon(self, val):
        if val:
            self.StartDeamonTower()
        else:
            self.Stop()

    def StartDeamonTower(self):
        self.AddOptionalActionsToDeamonTower()
        self.currSchema = DEAMON_TOWER
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
                else:
                    DebugPrint('Invalid stage')
                    return
            else:
                self.currStage = 0

            self.Start()
        else:
            self.currSchema = None            

    def AddOptionalActionsToDeamonTower(self):

        if DEAMON_TOWER['options']['UseBlacksmith']:
            action_dict = { 'args': [self.currSchema['options']['SlotToUpgrade']],
                          'function': ActionFunctions.UpgradeDeamonTower,
                          'requirements': {} }
                        
            DEAMON_TOWER['stages'][6]['actions'].append(action_dict)

        if DEAMON_TOWER['options']['GoAboveBlacksmith'] and player.LEVEL >= 75:
            action_dict = { 'args': [20348, (42500, 21600), [0, 0, 0]],
                          'function': ActionFunctions.TalkWithNPC,
                          'requirements': { ActionRequirementsCheckers.IS_IN_MAP: ['metin2_map_milgyo']}}
            DEAMON_TOWER['stages'][6]['actions'].append(action_dict)
        
        else:
            answer = []
            if player.LEVEL < 75:
                answer = [0, 0]
            else:
                answer = [0, 0, 2]

            action_dict = { 'args': [20348, (42500, 21600), answer],
                          'function': ActionFunctions.TalkWithNPC,
                          'requirements': { ActionRequirementsCheckers.IS_IN_MAP: ['metin2_map_milgyo']}}
            DEAMON_TOWER['stages'][6]['actions'].append(action_dict)

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


def switch_state():
    global instance
    instance.switch_state()

instance = AutoDungeon()