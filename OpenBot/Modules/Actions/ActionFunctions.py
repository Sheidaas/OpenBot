from time import sleep, time
from OpenBot.Modules import Movement, OpenLib
from OpenBot.Modules.Actions import ActionBot, ActionRequirementsCheckers
from OpenBot.Modules import NPCInteraction
from OpenBot.Modules.NPCInteraction import NPCAction
from OpenBot.Modules.OpenLog import DebugPrint
import eXLib
import player, net, chr, chat


def ClearFloor(args):
    player.SetAttackKeyState(False)
    x, y = args[0]
    my_x,my_y, z = player.GetMainCharacterPosition()
    path = eXLib.FindPath(my_x,my_y,x,y)
    if not path:
        return True
    is_monster_nearby = OpenLib.IsMonsterNearby()
    if OpenLib.isPlayerCloseToPosition(x, y) and not is_monster_nearby:
        return True

    if not is_monster_nearby:
        action_dict = {'args': [(x, y)], # position
        'function': MoveToPosition,
        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (x, y)},
        'on_failed': [ActionBot.NEXT_ACTION],
        }
        return action_dict

    vid = OpenLib.GetNearestMonsterVid()
    action_dict = {'args': [0, vid], # position
    'function': Destroy,
    'requirements': {},
    'on_success': [ActionBot.NEXT_ACTION],
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

    if eXLib.IsDead(instance_vid):
        player.SetAttackKeyState(False)
        return True

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
    if OpenLib.isPlayerCloseToPosition(position[0], position[1]):
        return True
    error = Movement.GoToPositionAvoidingObjects(position[0], position[1])
    if error != None:
        return True
    return False

def MoveToVID(args):
    x, y, z = chr.GetPixelPosition(args[0])
    return MoveToPosition([(x, y)])

def UsingItemOnInstance(args):
    instance = args[0]
    item_slot = args[1]
    if OpenLib.isPlayerCloseToInstance(instance):
        net.SendGiveItemPacket(instance, player.SLOT_TYPE_INVENTORY, item_slot, player.GetItemCount(item_slot))
        OpenLib.skipAnswers([0, 0], True)
        return True

    x, y, z = chr.GetPixelPosition(instance)
    action_dict = {'args': [(x, y)], # position
                    'function': MoveToPosition,
                    'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (x, y)},
                    'on_failed': [ActionBot.NEXT_ACTION],
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
                        'on_success': [ActionBot.NEXT_ACTION],
                        'on_failed': [ActionBot.NEXT_ACTION],
                        }
        return action_dict
        


    x, y = args[0]
    #DebugPrint('Clearing the floor')
    action_dict = { 'args': [(x, y)], # center position of area 
                    'function': ClearFloor,
                    'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (x, y, 100)},
                    'on_success': [ActionBot.NEXT_ACTION],
                    'on_failed': []
                }

    return action_dict

def UpgradeDeamonTower(args):
    item_slot = args[0]
    net.SendRefinePacket(item_slot, 4)
    return True

def GoBuyItemsFromNPC(args):
    items_slots_list_to_buy = args[0]
    npc_id = args[1]
    npc_position_x, npc_position_y = args[2]
    callback = args[3]

    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y)], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict

    npc = NPCAction(npc_id, event_answer=[1])
    NPCInteraction.RequestBusinessNPCClose(items_slots_list_to_buy, [], npc, callback)
    return True
    
def GetEnergyFromAlchemist(args):
    items_id_to_use = args[0]
    alchemist_id = args[1]
    npc_position_x, npc_position_y = args[2]
    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y), 250], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict
    

    for _id in items_id_to_use:
        item_slot = OpenLib.GetItemByID(_id)
        if item_slot < 0:
            continue
        alchemist_vid = OpenLib.GetInstanceByID(alchemist_id)
        if alchemist_vid != -1:
            action_dict = {'args': [alchemist_vid, item_slot], # position
                            'function': UsingItemOnInstance,
                            'requirements': {},
                            'on_success': [ActionBot.NEXT_ACTION],
                            'on_failed': [ActionBot.NEXT_ACTION],
                            }
            return action_dict

    
    return True

def ChangeEnergyToCrystal(args):
    alchemist_id = args[0]
    npc_position_x, npc_position_y = args[1]
    map_name = args[2]
    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'args': [(npc_position_x, npc_position_y), 250], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)},
                        'on_success': [],
                        }
        return action_dict
    energy_crystal = OpenLib.GetItemByID(51001)
    if player.GetItemCount(energy_crystal) >= 30:
        answer = [5,254,254,0,254]
        action_dict = { 'args': [alchemist_id, (npc_position_x, npc_position_y), answer, map_name], # ID, event_answer, posiiton of npc, npc's map
                          'function': TalkWithNPC,
                          'on_success': [],
                          'requirements': {},

            }
        return action_dict
    return True

def TalkWithNPC(args):
    npc_id = args[0]
    player_position_x, player_position_y = args[1]
    event_answer = args[2]
    map_name = args[3]
    vid = OpenLib.GetInstanceByID(npc_id)
    npc_position_x, npc_position_y, z = chr.GetPixelPosition(vid)
    if not ActionRequirementsCheckers.isInMaps([map_name]):
        return True
    if not OpenLib.isPlayerCloseToPosition(player_position_x, player_position_y, 500):
        action_dict = {'args': [(player_position_x, player_position_y), 250], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict
    
    if vid >= 0:
        net.SendOnClickPacket(vid)
        OpenLib.skipAnswers(event_answer, False)
        chat.AppendChat(3, str(vid))
        return True
    return False
    
def MineOre(args):
    selectedOre = args[0]
    is_curr_mining = args[1]()
    #if eXLib.IsDead(selectedOre):
    #    return True
    #
    #if not OpenLib.IsWeaponPickaxe():
    #    return True
    if not OpenLib.isPlayerCloseToInstance(selectedOre):
        action_dict = {'args': [selectedOre],
                        'function': MoveToVID,
                        'requirements': {ActionRequirementsCheckers.isNearInstance: [selectedOre]},
                        'on_success': [ActionBot.NEXT_ACTION]}
        return action_dict
                    
    if not is_curr_mining:
        net.SendOnClickPacket(selectedOre)
    
    return False
    
def LookForBlacksmithInDeamonTower(args):
    go_above_six_stage = args[0]
    item_index_to_upgrade = args[1]

    blacksmiths_id = [20074, 20075, 20076]

    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        for _id in blacksmiths_id:
            if chr.GetRace() == _id:
                
                if not OpenLib.isPlayerCloseToInstance(vid):
                    action_dict = {
                        'args': [vid],
                        'function': MoveToVID,
                        'requirements': { ActionRequirementsCheckers.IS_NEAR_INSTANCE: vid},
                        'on_failed': [ActionBot.NEXT_ACTION]
                    }

                    return action_dict

                if item_index_to_upgrade >= 0:
                    UpgradeDeamonTower(item_index_to_upgrade)
                
                if go_above_six_stage:
                    if player.GetStatus(player.LEVEL) < 75:
                        answer = [0, 0]
                    else:
                        answer = [0, 0, 0]
                
                else:
                    if player.GetStatus(player.LEVEL) < 75:
                        answer = [0, 0]
                    else:
                        answer = [2, 0, 0]

                blacksmith_x, blacksmith_y, blacksmith_z = chr.GetPixelPosition(vid)
                action_dict = {
                    'args': [_id, (blacksmith_x, blacksmith_y), answer, 'metin2_map_deviltower1'],
                    'function': TalkWithNPC,
                    'on_success': [],
                    'requirements': {},
                }
                return action_dict

            
    return False