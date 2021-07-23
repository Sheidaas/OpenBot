from OpenBot.Modules.DmgHacks import Pause
from OpenBot.Modules.OpenLog import DebugPrint
from BotBase import BotBase
from NPCInteraction import NPCAction
import UIComponents, OpenLog, Movement, OpenLib
import ui, player, background, chat, chr, net
import eXLib
import DmgHacks

#
#DT Blacksmith 20074
#DT Weapon Blacksmith 20075
#DT Jewelry Blacksmith 20076
#Demontower 20348
# METIN POS 14080 64335


# REQUIREMENTS
IS_NEAR_POSITION = 'isNearPosition'
IS_ON_POSITION = 'isOnPosition'
IS_IN_MAP = 'isInMap'
# ON_SUCCESS FLAGS
NEXT_ACTION = 'next_action'

# ON ACTION RETURN FLAGS
DISCARD = 'discard'

# STATES
STATE_CANCELING = -2
STATE_STOP = -1
STATE_CHOOSING_DUNGEON = 0
STATE_DOING_DUNGEON = 1

# ACTIONS

def ClearFloor(args):
    player.SetAttackKeyState(False)
    x, y = args[0]
    my_x,my_y,z = player.GetMainCharacterPosition()
    path = eXLib.FindPath(my_x,my_y,x,y)
    if not path:
        return True
    is_monster_nearby = OpenLib.IsMonsterNearby()
    if OpenLib.isPlayerCloseToPosition(x, y) and not is_monster_nearby:
        return True
    if not is_monster_nearby:
        action_dict = {'args': [(x, y)], # position
        'function': MoveToPosition,
        'requirements': { IS_ON_POSITION: (x, y)},
        'on_failed': [NEXT_ACTION],
        }
        return action_dict

    vid = OpenLib.GetNearestMonsterVid()
    action_dict = {'args': [0, vid], # position
    'function': Destroy,
    'requirements': {},
    'on_success': [NEXT_ACTION],
    }
    return action_dict

def Destroy(args):
    if args[1]:
        instance_vid = args[1]
    else:
        instance_vid = 0
        for vid in eXLib.InstancesList:
            chr.SelectInstance(vid)
            if chr.GetRace() == args[0]:
                instance_vid = vid
                break


    vid_life_status = OpenLib.AttackTarget(instance_vid)

    if vid_life_status == OpenLib.TARGET_IS_DEAD:
        player.SetAttackKeyState(False)
        return True

    elif vid_life_status == OpenLib.ATTACKING_TARGET:
        return False

    elif vid_life_status == OpenLib.MOVING_TO_TARGET:
        return False
    
    return False

def Find(args):
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if chr.GetRace() == args[0]:
            return True
    return False

def MoveToPosition(args):
    position = args[0]
    error = Movement.GoToPositionAvoidingObjects(position[0], position[1])
    if error != None:
        return True
    return False

def EnterMapByNPC(args):
    action = NPCAction(args[0], event_answer=args[1], position=args[2], _map=args[3])
    action.GoToPosition(callback=action.DoAction)
    return True

def UsingItemOnInstance(args):
    instance = args[0]
    item_slot = args[1]
    if OpenLib.isPlayerCloseToInstance(instance):
        net.SendGiveItemPacket(instance ,player.SLOT_TYPE_INVENTORY, item_slot, player.GetItemCount(item_slot))
        return True

    x, y, z = chr.GetPixelPosition(instance)
    action_dict = {'args': [(x, y)], # position
                    'function': MoveToPosition,
                    'requirements': { IS_ON_POSITION: (x, y)},
                    'on_failed': [NEXT_ACTION],
                    }
    return action_dict

def OpenAllSeals(args): # center position of floor, 
    #DebugPrint('Launch OpenAllSeals')
    closest_seal = OpenLib.getClosestInstance([OpenLib.OBJECT_TYPE])
    #DebugPrint('Closest seal ' + str(closest_seal))
    if closest_seal < 0:
        #DebugPrint('There is no seal to open')
        return True

    slot_with_key = OpenLib.GetItemByID(50084)
    if slot_with_key >= 0:
        #DebugPrint('Char has an stone key')
        #DebugPrint('Using item on seal')
        action_dict = {'args': [closest_seal, slot_with_key], # position
                        'function': UsingItemOnInstance,
                        'requirements': {},
                        'on_success': [NEXT_ACTION],
                        'on_failed': [NEXT_ACTION],
                        }
        return action_dict
        


    x, y = args[0]
    #DebugPrint('Clearing the floor')
    action_dict = { 'args': [(x, y)], # center position of area 
                    'function': ClearFloor,
                    'requirements': {IS_NEAR_POSITION: (x, y, 100)},
                    'on_success': [NEXT_ACTION],
                    'on_failed': []
                }
    return action_dict

def UpgradeDeamonTower(args):
    item_slot = args[0]
    net.SendRefinePacket(item_slot, 4)
    return True

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
        0: { # stage in hwang temple, entering dt
            'actions': [{ 'args': [20348, [0, 0], (53200, 59600), 'metin2_map_milgyo'], # ID, event_answer, posiiton of npc, npc's map
                          'function': EnterMapByNPC,
                          'requirements': { IS_IN_MAP: ['metin2_map_deviltower1'] }

            }]},
        1: { # stage with metin
            'actions': [{'args': [(19004, 69011)], # position
                        'function': MoveToPosition,
                        'requirements': { IS_ON_POSITION: (19004, 69011)}
                        },
                        {'args': [8015],
                        'function': Find,
                        'requirements': {},
                        'on_success': [NEXT_ACTION],
                        'on_failed': []
                        },
                        {'args': [8015, 0],
                        'function': Destroy,
                        'requirements': {IS_NEAR_POSITION: (12599, 38399, 1000)},
                        'on_success': [NEXT_ACTION],
                        'on_failed': []
                        }]},
        2: { # stage with only deamons
            'actions': [{ 'args': [(15003, 40961)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ClearFloor,
                          'requirements': {IS_NEAR_POSITION: (13400, 14700, 1000)}, #
                          'on_success': [NEXT_ACTION],
                          'on_failed': [NEXT_ACTION]
                        }],},
        3: { # stage with king
            'actions': [{ 'args': [(17688, 19619)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ClearFloor,
                          'requirements': {IS_NEAR_POSITION: (37037, 62659, 2000)}, # 
                          'on_success': [NEXT_ACTION],
                          'on_failed': [NEXT_ACTION]
                        }],},
        4: { # stage with metins
            'actions': [{ 'args': [(39123, 65131)], # ID, event_answer, posiiton of npc, npc's map
                          'function': ClearFloor,
                          'requirements': {IS_NEAR_POSITION: (39539, 43607, 5000)}, # IS_NEAR_POSITION: (37722, 63632, 1000)
                          'on_success': [NEXT_ACTION],
                          'on_failed': [NEXT_ACTION]
                        }],},
        5: { # stage with keys
            'actions': [{ 'args': [(40000, 44000)], # ID, event_answer, posiiton of npc, npc's map
                          'function': OpenAllSeals,
                          'requirements': {IS_NEAR_POSITION: (40713, 19914, 5000)},
                          'on_success': [NEXT_ACTION],
                          'on_failed': []
                        }],},
        6: { # stage with blacksmith
            'actions': [{ 'args': [(41000, 20000)],
                          'function': ClearFloor,
                          'requirements': {},
                          'on_success': [NEXT_ACTION],
                          'on_failed': []
                        }

                        ],},
        },
        7: { # stage with metins and chests
            'actions': [{ 'args': [(61500, 20000)],
                          'function': ClearFloor,
                          'requirements': {}, # DONT NEED ANY
                          'on_success': [NEXT_ACTION],
                          'on_failed': []
                        }

                        ],
        },
        8: { # stage with keys
            'actions': [{ 'args': [(61690, 42200)],
                          'function': ClearFloor,
                          'requirements': {IS_NEAR_POSITION: (40713, 19914, 5000)}, # DONT NEED ANY
                          'on_success': [NEXT_ACTION],
                          'on_failed': []
                        }

                        ],
        },
        9: { # ripper
            'actions': [{ 'args': [(61690, 61690)],
                          'function': ClearFloor,
                          'requirements': {}, # DONT NEED ANY
                          'on_success': [NEXT_ACTION],
                          'on_failed': []
                        }

                        ],
        },
        }

def getCallBackWithArg(func, arg):
    return lambda: func(arg)

class AutoDungeon(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.currSchema = None
        self.currState = STATE_CHOOSING_DUNGEON
        self.currStage = 0
        self.currAction = 0

        self.currActionDict = None
        self.currActionsDictsQueue = []

        self.options = {
            'UseDmgHack': False,
            'NextChannelIfThereIsAnotherPlayer': False
        }

        self.BuildWindow()

    def BuildWindow(self):
        self.comp = UIComponents.Component()
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

        self.showUseDmgHackButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tUse DMG Hack', '', 20, 30, funcState=self.switch_use_dmg_hack, defaultValue=self.options['UseDmgHack'])
        self.showNextChannelIfThereIsAnotherPlayerButton = comp.OnOffButton(self.settings_tab, '\t\t\t\t\t\tAvoid players', '', 20, 50, funcState=self.switch_use_dmg_hack, defaultValue=self.options['NextChannelIfThereIsAnotherPlayer'])

    def switch_use_dmg_hack(self, val):
        self.options['useDmgHack'] = val
        if not val:
            DmgHacks.Pause()

    def switch_next_channel_if_there_is_another_player(self, val):
        self.options['NextChannelIfThereIsAnotherPlayer'] = val

    def switch_launch_auto_dungeon(self, val):
        if val:
            self.StartDeamonTower()
        else:
            self.Stop()

    def StartDeamonTower(self):
        self.currSchema = DEAMON_TOWER
        if self.CheckRequirementsForCurrSchema():

            if str(background.GetCurrentMapName()) == 'metin2_map_deviltower1':
                if self.isNearPosition((19004, 69011, 10000)):
                    self.currStage = 1
                elif self.isNearPosition((12599, 38399, 10000)):
                    self.currStage = 2
                elif self.isNearPosition((18000, 18000, 10000)):
                    self.currStage = 3
                elif self.isNearPosition((37037, 62659, 10000)):
                    self.currStage = 4
                elif self.isNearPosition((39539, 43607, 10000)):
                    self.currStage = 5
                elif self.isNearPosition((40713, 19914, 10000)):
                    self.currStage = 6
                else:
                    DebugPrint('Invalid stage')
                    return
            else:
                self.currStage = 0

            self.AddOptionalActionsToDeamonTower()
            self.currState = STATE_DOING_DUNGEON
            self.Start()
        else:
            self.currSchema = None            

    def AddOptionalActionsToDeamonTower(self):
        if self.currSchema['options']['UseBlacksmith']:
            action_dict = { 'args': [self.currSchema['options']['SlotToUpgrade']],
                          'function': UpgradeDeamonTower,
                          'requirements': {} }
            self.currSchema['stages'][6]['actions'].append(action_dict)

        if self.currSchema['options']['GoAboveBlacksmith'] and player.LEVEL >= 75:
            action_dict = { 'args': [20348, [0, 0, 0], (42500, 21600), 'metin2_map_deviltower1'],
                          'function': EnterMapByNPC,
                          'requirements': { IS_IN_MAP: ['metin2_map_milgyo']}}
            self.currSchema['stages'][6]['actions'].append(action_dict)
        else:
            answer = []
            if player.LEVEL < 75:
                answer = [0, 0]
            else:
                answer = [0, 0, 2]

            action_dict = { 'args': [20348, answer, (42500, 21600), 'metin2_map_deviltower1'],
                          'function': EnterMapByNPC,
                          'requirements': { IS_IN_MAP: ['metin2_map_milgyo']}}
            self.currSchema['stages'][6]['actions'].append(action_dict)

    def CheckRequirementsForCurrSchema(self):
        for requirement in self.currSchema['requirements'].keys():

            if requirement == 'lvl':
                if self.isAboveLVL(self.currSchema['requirements'][requirement]):
                    chat.AppendChat(3, '[AutoDungeon] You have ' + str(player.LEVEL) + ' lvl but you need ' + str(self.currSchema['requirements'][requirement]))
                    return False

            if requirement == 'inInMap':
                if not self.isInMaps(self.currSchema['requirements'][requirement]):
                    chat.AppendChat(3, '[AutoDungeon] You need to be atleast on this maps: ' + str(self.currSchema['requirements'][requirement]))
                    return False
            
            if requirement == 'isOnPosition':
                if not self.inOnPosition(self.currSchema['requirements'][requirement]):
                    chat.AppendChat(3, '[AutoDungeon] You need to be on this position: ' + str(self.currSchema['requirements'][requirement]))
                    return False
            
        return True

    def CheckRequirementsForCurrAction(self):
        if self.currActionDict != None:
            requirements = self.currActionDict['requirements']
        else:
            requirements = self.currSchema['stages'][self.currStage]['actions'][self.currAction]['requirements']

        for requirement in requirements:

            if requirement == IS_IN_MAP:
                if not self.isInMaps(requirements[requirement]):
                    return False
            
            if requirement == IS_ON_POSITION:
                if not self.isOnPosition(requirements[requirement]):
                    return False
            
            if requirement == IS_NEAR_POSITION:
                if not self.isNearPosition(requirements[requirement]):
                    return False

        return True

    def GoToNextAction(self, skipRequirements=False):
        if skipRequirements:
            if self.currActionDict != None:
                self.currActionDict = None
                if self.currActionsDictsQueue:
                    self.currActionDict = self.currActionsDictsQueue.pop(0)

                OpenLog.DebugPrint(str(self.currActionDict['function'])+ ' SUCCESS ADD ACTION SKIPPED')
            else:
                if self.currAction + 1 < len(self.currSchema['stages'][self.currStage]['actions']):
                    self.currAction += 1
                    OpenLog.DebugPrint(str(self.currSchema['stages'][self.currStage]['actions'][self.currAction]['function']) + ' SUCCESS SCHEME ACTION SKIPPED')
                else:
                    OpenLog.DebugPrint('Stage Complete')
                    self.GoToNextStage()
        else:
            if self.CheckRequirementsForCurrAction():
                if self.currActionDict != None:
                    self.currActionDict = None
                    if self.currActionsDictsQueue:
                        self.currActionDict = self.currActionsDictsQueue.pop(0)
                    DebugPrint(str(self.currActionDict['function']) + ' SUCCESS ADD ACTION')
                else:
                    if self.currAction + 1 < len(self.currSchema['stages'][self.currStage]['actions']):
                        self.currAction += 1
                        DebugPrint(str(self.currSchema['stages'][self.currStage]['actions'][self.currAction]['function']) + ' SUCCESS SCHEME ACTION')
                    else:
                        chat.AppendChat(3, 'Stage Complete')
                        self.GoToNextStage()

    def GoToNextStage(self):
        self.currAction = 0
        if self.currStage + 1 < len(self.currSchema['stages']):
            self.currStage += 1
        else:
            OpenLog.DebugPrint('Dungeon Complete')
            self.Stop()

    def DoAction(self, action_dict):
        args = action_dict['args']
        action = action_dict['function']
        if action.__name__ in [Destroy.__name__, ClearFloor.__name__, OpenAllSeals.__name__] and self.options['useDmgHack']:
            DmgHacks.Resume()
        else:
            if DmgHacks.IsOn():
                DmgHacks.Pause()
        return action(args)

    def isAboveLVL(self, lvl):
        if int(player.LEVEL) < lvl:
            return False
        return True
    
    def isInMaps(self, maps):
        for mapName in maps:
            if str(background.GetCurrentMapName()) == mapName:
                return True
        return False

    def isNearPosition(self, position):
        return OpenLib.isPlayerCloseToPosition(position[0], position[1], position[2])

    def isOnPosition(self, position):
        x, y = position
        if OpenLib.isPlayerCloseToPosition(x, y, max_dist=150):
            return True
        return False

    def StopBot(self):
        self.currSchema = None
        self.currStage = 0
        self.currAction = 0
        self.currActionsDictsQueue = []
        self.currActionDict = None
        self.currState = STATE_CHOOSING_DUNGEON
        DmgHacks.Pause()

    def Frame(self):
        if self.currActionDict != None:
            OpenLog.DebugPrint('Added action')
            action_dict = self.currActionDict
        else:
            action_dict = self.currSchema['stages'][self.currStage]['actions'][self.currAction]
            OpenLog.DebugPrint(str(self.currSchema['stages'][self.currStage]['actions'][self.currAction]) + ' Scheme action')

        is_action_done = self.DoAction(action_dict)
        if is_action_done is True or is_action_done is False:

            if 'on_success' in action_dict.keys() and is_action_done:
                OpenLog.DebugPrint(str(action_dict['function']) + ' SUCCESS_CASE')
                if NEXT_ACTION in action_dict['on_success']:
                    self.GoToNextAction()

            elif 'on_failed' in action_dict.keys() and not is_action_done:
                OpenLog.DebugPrint(str(action_dict['function']) + ' FAILED_CASE')
                if NEXT_ACTION in action_dict['on_failed']:
                    self.GoToNextAction(skipRequirements=True)
            
            else:
                OpenLog.DebugPrint(str(action_dict['function']) + ' CHECKING REQ')
                self.GoToNextAction()
        else:
            if self.currActionDict != None:
                self.currActionsDictsQueue.append(self.currActionDict)

            self.currActionDict = is_action_done

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()


def switch_state():
    global instance
    instance.switch_state()

instance = AutoDungeon()