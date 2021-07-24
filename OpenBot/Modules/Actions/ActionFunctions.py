import Movement, OpenLib
from OpenBot.Modules.Actions import ActionBot
from NPCInteraction import NPCAction
import eXLib
import player, net


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
        'requirements': { ActionBot.IS_ON_POSITION: (x, y)},
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
        net.SendGiveItemPacket(instance, player.SLOT_TYPE_INVENTORY, item_slot, player.GetItemCount(item_slot))
        return True

    x, y, z = chr.GetPixelPosition(instance)
    action_dict = {'args': [(x, y)], # position
                    'function': MoveToPosition,
                    'requirements': { ActionBot.IS_ON_POSITION: (x, y)},
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
                    'requirements': {ActionBot.IS_NEAR_POSITION: (x, y, 100)},
                    'on_success': [ActionBot.NEXT_ACTION],
                    'on_failed': []
                }
    return action_dict

def UpgradeDeamonTower(args):
    item_slot = args[0]
    net.SendRefinePacket(item_slot, 4)
    return True
