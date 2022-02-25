from OpenBot.Modules import MapManager, Movement, OpenLib
from OpenBot.Modules.Actions import Action, ActionRequirementsCheckers
from OpenBot.Modules import NPCInteraction
from OpenBot.Modules.NPCInteraction import NPCAction
from OpenBot.Modules.OpenLog import DebugPrint
import eXLib
import player, net, chr, background, item, chat


# Standard
def ClearFloor(args):
    player.SetAttackKeyState(False)
    x, y = args[0]
    my_x,my_y, z = player.GetMainCharacterPosition()
    path = eXLib.FindPath(my_x,my_y,x,y)
    if not path:
        Movement.StopMovement()
        return True
    is_monster_nearby = OpenLib.IsMonsterNearby()
    if OpenLib.isPlayerCloseToPosition(x, y) and not is_monster_nearby:
        Movement.StopMovement()
        return True

    if not is_monster_nearby:
        action_dict = {'function_args': [(x, y)], # position
        'name': 'Go to center of floor',
        'function': MoveToPosition,
        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (x, y)},
        'on_failed': [Action.NEXT_ACTION],
        }
        return action_dict

    vid = OpenLib.GetNearestMonsterVid()
    action_dict = {'function_args': [vid], # position
    'function': DestroyByVID,
    'name': 'Kill mob',
    'requirements': {},
    'on_success': [Action.NEXT_ACTION],
    }
    return action_dict


def DestroyByVID(args):
    instance_vid = args[0]
    if instance_vid not in eXLib.InstancesList:
        return True

    if eXLib.IsDead(instance_vid):
        player.SetAttackKeyState(False)
        return Action.NEXT_ACTION

    if not OpenLib.isPlayerCloseToInstance(instance_vid, 300):
        x, y, z = chr.GetPixelPosition(instance_vid)
        action_dict = {
            'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [x, y, 200],
                             ActionRequirementsCheckers.IS_IN_MAP: [background.GetCurrentMapName()]},
            'function': MoveToPosition,
            'function_args': [(x, y)],
            'name': 'Going to enemy',
            'interruptors_args': [instance_vid, instance_vid],
            'interruptors': [ActionRequirementsCheckers.isVidNearly, ActionRequirementsCheckers.IsVidNotExist],
            'interrupt_function': lambda : Action.NEXT_ACTION
        }
        return action_dict

    vid_life_status = OpenLib.AttackTarget(instance_vid)

    if vid_life_status == OpenLib.TARGET_IS_DEAD:
        player.SetAttackKeyState(False)
        return Action.NEXT_ACTION

    elif vid_life_status == OpenLib.ATTACKING_TARGET:
        return Action.NOTHING

    elif vid_life_status == OpenLib.MOVING_TO_TARGET:
        return Action.NOTHING
    
    return False


def DestroyByID(args):
    instance_id = args[0]
    instance_vid = OpenLib.GetVIDByClosestNPC(instance_id)
    if instance_vid not in eXLib.InstancesList:
        return False

    if not OpenLib.isPlayerCloseToInstance(instance_vid, 200):
        x, y, z = chr.GetPixelPosition(instance_vid)
        action_dict = {
            'function': MoveToPosition,
            'function_args': [(x, y)],
            'name': 'Going to enemy',
        }
        return action_dict
        
    vid_life_status = OpenLib.AttackTarget(instance_vid)

    if vid_life_status == OpenLib.TARGET_IS_DEAD:
        player.SetAttackKeyState(False)
        return Action.NEXT_ACTION

    elif vid_life_status == OpenLib.ATTACKING_TARGET:
        return Action.NOTHING

    elif vid_life_status == OpenLib.MOVING_TO_TARGET:
        return Action.NOTHING
    
    return False


def MoveToPosition(args):
    player.SetAttackKeyState(False)
    position = args[0]


    if len(args) > 1:
        if args[1] == background.GetCurrentMapName() and not OpenLib.is_straight_line_blocked_to_position(position[0], position[1]):
            Movement.mapMovement.MoveToMapPosition(position, maxDist=150)
            return True
        else:
            error = Movement.GoToPositionAvoidingObjects(position[0], position[1], mapName=args[1])
    else:
        if OpenLib.is_straight_line_blocked_to_position(position[0], position[1]):
            Movement.mapMovement.MoveToMapPosition(position, maxDist=150)
            return True
        else:
            error = Movement.GoToPositionAvoidingObjects(position[0], position[1], mapName=background.GetCurrentMapName())

    if error == Movement.NO_PATH_FOUND:
        return Action.ERROR
    
    elif error == Movement.MOVING:
        return True
    
    elif error == Movement.DESTINATION_REACHED:
        return Action.NEXT_ACTION


    #DebugPrint('Going to ' + str(position))


def MoveToPositionByVid(args):
    vid = args[0]
    player.SetAttackKeyState(False)
    x, y, z = chr.GetPixelPosition(vid)
    if not OpenLib.is_straight_line_blocked_to_vid(vid):
        Movement.mapMovement.MoveToMapPosition((x, y), maxDist=175)
        return True
    else:
        error = Movement.GoToPositionAvoidingObjects(x, y, maxDist=150, mapName=background.GetCurrentMapName())

        if error == Movement.NO_PATH_FOUND:
            return Action.ERROR

        elif error == Movement.MOVING:
            return True

        elif error == Movement.DESTINATION_REACHED:
            return Action.NEXT_ACTION



def UseItemOnNPC(args):
    npc_id = args[0]
    item_slot = args[1]

    npc_position = MapManager.GetNpcFromMap(background.GetCurrentMapName(), npc_id)

    if not OpenLib.isPlayerCloseToPosition(npc_position[0], npc_position[1], 500):
        action_dict = {'function_args': [(npc_position[0], npc_position[1])], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position[0], npc_position[1])},
                        'on_failed': [Action.NEXT_ACTION],
                        }   
        return action_dict

    vid = OpenLib.GetVIDByClosestNPC(npc_id)    
    net.SendGiveItemPacket(vid, player.SLOT_TYPE_INVENTORY, item_slot, player.GetItemCount(item_slot))
    OpenLib.skipAnswers([0, 0], True)
    return True         


def GoBuyItemsFromNPC(args):
    from OpenBot.Modules.InstanceInteractions.shopper_module import NPC_EVENT_ANSWERS
    items_slots_list_to_buy = args[0]
    npc_id = args[1]
    event_answer = args[2]
    callback = args[3]
    current_map = background.GetCurrentMapName()
    if current_map == OpenLib.GetPlayerEmpireFirstMap() or current_map == OpenLib.GetPlayerEmpireSecondMap():
        pass
    else:
        try:
            closest_map = MapManager.GetClosestMapPathWithNPC(npc_id)[:-1][0][0].GetDestMap()
        except:
            closest_map = ''
        if not closest_map:
            current_map = OpenLib.GetPlayerEmpireFirstMap()


    npc_position_x, npc_position_y = MapManager.GetNpcFromMap(current_map, npc_id)
    if not OpenLib.isPlayerCloseToPosition(npc_position_x, npc_position_y):
        action_dict = {'function_args': [(npc_position_x, npc_position_y), current_map], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (npc_position_x, npc_position_y)}
                        }
        return action_dict

    DebugPrint(str(items_slots_list_to_buy))
    npc = NPCAction(npc_id, event_answer=NPC_EVENT_ANSWERS[npc_id])
    NPCInteraction.RequestBusinessNPCClose(items_slots_list_to_buy, [], npc, callback)
    return True


def TalkWithNPC(args):
    npc_id = args[0]
    event_answer = args[1]
    map_name = args[2]
    result = MapManager.GetNpcFromMap(map_name, npc_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1], 1000):
        action_dict = {'function_args': [(result[0], result[1]), map_name], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_NEAR_POSITION: (result[0], result[1], 1000),
                                          ActionRequirementsCheckers.IS_IN_MAP: [map_name]}
                        }
        return action_dict
    
    vid = OpenLib.GetInstanceByID(npc_id)
    if vid >= 0:
        net.SendOnClickPacket(vid)
        OpenLib.skipAnswers(event_answer, True)
        return True
    return False


def ChangeChannel(args):
    channel_id = args[0]

    from OpenBot.Modules.ChannelSwitcher import channel_switcher_interface

    if not channel_id:
        DebugPrint('Channel id is ' + str(channel_id))
        return Action.ERROR

    if OpenLib.GetCurrentChannel() == channel_id:
        return Action.NEXT_ACTION

    if 0 < channel_id > len(channel_switcher_interface.channel_switcher_interface.GetChannels()):
        return Action.ERROR
    

    if channel_switcher_interface.channel_switcher_interface.GetCurrentState() != channel_switcher_interface.STATE_CHANGING_CHANNEL:
        DebugPrint('Changing channel to ' + str(channel_id) )
        channel_switcher_interface.channel_switcher_interface.ConnectToChannelByID(channel_id)
        return {
            'name': 'Waiting to change channel',
            'function': WaitFor,
            'function_args': [0],
            'requirements': {ActionRequirementsCheckers.IS_IN_CHANNEL: channel_id}
        }

def ImproveRod(args):
    npc_id = 9009
    map_name = background.GetCurrentMapName()
    result = MapManager.GetNpcFromMap(map_name, npc_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1], 1000):
        action_dict = {'function_args': [(result[0], result[1]), map_name],  # position
                       'function': MoveToPosition,
                       'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (result[0], result[1], 1000),
                                        ActionRequirementsCheckers.IS_IN_MAP: [map_name]}
                       }
        return action_dict

    net.SendItemUsePacket(player.EQUIPMENT,item.EQUIPMENT_WEAPON)
    vid = OpenLib.GetInstanceByID(npc_id)
    slot = OpenLib.GetItemByType(item.ITEM_TYPE_ROD)
    if not slot:
        return False
    net.SendGiveItemPacket(vid, player.SLOT_TYPE_INVENTORY, slot, player.GetItemCount(slot))

    OpenLib.skipAnswers([0, 0], True)
    return True


def GoSellItemsToNPC(args):
    from OpenBot.Modules.InstanceInteractions import shopper_module
    npc_id = args[1]
    slots_to_sell = args[0]
    callback = args[3]
    map_name = background.GetCurrentMapName()
    if map_name != OpenLib.GetPlayerEmpireFirstMap() or map_name != OpenLib.GetPlayerEmpireSecondMap():
        map_name = OpenLib.GetPlayerEmpireFirstMap()
    result = MapManager.GetNpcFromMap(map_name, npc_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1], 1000):
        action_dict = {
                        'name': 'Selling items',
                        'function_args': [(result[0], result[1]), map_name],  # position
                       'function': MoveToPosition,
                       'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (result[0], result[1], 1000),
                                        ActionRequirementsCheckers.IS_IN_MAP: [map_name]}
                       }
        return action_dict
    npc = NPCAction(npc_id, event_answer=shopper_module.NPC_EVENT_ANSWERS[npc_id])
    NPCInteraction.RequestBusinessNPCClose([], slots_to_sell, npc, callback)
    return True



def GrillFish(args):
    npc_id = args[1]
    slots_to_grill = args[0]
    map_name = background.GetCurrentMapName()

    camp_vid = -1
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if chr.GetRace() == 12000:
            camp_vid = vid
            break

    if camp_vid == -1:
        chat.AppendChat(3, 'There is no grill')
        return False

    x, y, z = chr.GetPixelPosition(camp_vid)
    result = [x, y]
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1], 1000):
        action_dict = {'function_args': [(result[0], result[1]), map_name],  # position
                       'function': MoveToPosition,
                       'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (result[0], result[1], 1000),
                                        ActionRequirementsCheckers.IS_IN_MAP: [map_name]}
                       }
        return action_dict

    for slots in OpenLib.GetItemsSlotsByID(slots_to_grill).values():
        for slot in slots:
            chat.AppendChat(3, str(camp_vid) + ' ' + str(slot))
            net.SendGiveItemPacket(camp_vid, player.SLOT_TYPE_INVENTORY, slot, player.GetItemCount(slot))
    return Action.NEXT_ACTION


# Utils
def ChangeMap(args):
    move_position_x, move_position_y = args[0]
    map_name = args[1]
    npc_id = args[2]
    event_answer = args[3]
    map_destination_name = args[4]


    DebugPrint('Changing the map')
    if map_name == background.GetCurrentMapName() and not npc_id and not event_answer:
        DebugPrint('Going go position')
        if not OpenLib.isPlayerCloseToPosition(move_position_x, move_position_y):
            DebugPrint('Returning move to position action')
            return {
                'function_args': [(move_position_x, move_position_y), map_name],
                'name': 'Going to teleport point',
                'function': MoveToPosition,
                'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [move_position_x, move_position_y]}
            }
        DebugPrint('going to next actions')
        return True

    elif map_name == background.GetCurrentMapName() and npc_id and event_answer:
        DebugPrint(map_destination_name + ' ' + map_name + ' ' + background.GetCurrentMapName())
        DebugPrint('Returning talk with npc')
        result = MapManager.GetNpcFromMap(map_name, npc_id)
        if result is None:
            return Action.NEXT_ACTION
        if not OpenLib.isPlayerCloseToPosition(result[0], result[1], 1000):
            action_dict = {'function_args': [(result[0], result[1]), map_name],  # position
                           'function': MoveToPosition,
                           'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (result[0], result[1], 1000),
                                            ActionRequirementsCheckers.IS_IN_MAP: [map_name]}
                           }
            return action_dict

        vid = OpenLib.GetInstanceByID(npc_id)
        if vid >= 0:
            net.SendOnClickPacket(vid)
            OpenLib.skipAnswers(event_answer, True)
            return True
        return False
    return Action.NEXT_ACTION
    

def WaitFor(args):
    if not len(args) > 1:
        return True
    from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
    modules_to_switch_off = args[1]
    if 'waithack' in modules_to_switch_off:
        waithack_interface.Stop()
    return True

# Alchemist 
def BuyItemsForAlchemist(args):
    npc_id = int(args[0])
    map_name = args[1]
    callback = args[2]
    result = MapManager.GetNpcFromMap(map_name, npc_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1]):
        action_dict = {'function_args': [(result[0], result[1]), map_name], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (result[0], result[1])}
                        }
        return action_dict
    items_to_buy = [4 for x in range(OpenLib.GetNumberOfFreeSlots())]    
    npc = NPCAction(npc_id, event_answer=[1])
    NPCInteraction.RequestBusinessNPCClose(items_to_buy, [], npc, callback)
    return True  

def ExchangeItemsForAlchemist(args):
    item_list = args[0]
    npc_id = int(args[1])
    map_name = args[2]
    result = MapManager.GetNpcFromMap(map_name, npc_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1]):
        action_dict = {'function_args': [(result[0], result[1]), map_name], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (result[0], result[1])}
                        }
        return action_dict
    for _id in item_list:
        item_slot = OpenLib.GetItemByID(int(_id))
        if item_slot < 0:
            continue
        action_dict = {'function_args': [npc_id, item_slot], # position
                        'function': UseItemOnNPC,
                        'on_success': [Action.NEXT_ACTION],
                        'on_failed': [Action.NEXT_ACTION],
                        }
        return action_dict
    return Action.NEXT_ACTION

def GetEnergyFromAlchemist(args):
    items_id_to_use = args[0]
    alchemist_id = int(args[1])
    map_name = args[2]
    result = MapManager.GetNpcFromMap(map_name, alchemist_id)
    if result is None:
        return Action.NEXT_ACTION
    if not OpenLib.isPlayerCloseToPosition(result[0], result[1]):
        action_dict = {'function_args': [(result[0], result[1]), map_name], # position
                        'function': MoveToPosition,
                        'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (result[0], result[1])}
                        }
        return action_dict
    

    for _id in items_id_to_use:
        item_slot = OpenLib.GetItemByID(int(_id))
        if item_slot < 0:
            continue
        action_dict = {'function_args': [alchemist_id, item_slot], # position
                        'function': UseItemOnNPC,
                        'on_success': [Action.NEXT_ACTION],
                        'on_failed': [Action.NEXT_ACTION],
                        }
        return action_dict
    return True

# Farmbot
def MineOre(args):
    selectedOre = args[0]
    is_curr_mining = args[1]()
    if selectedOre not in eXLib.InstancesList:
        return Action.NEXT_ACTION
    
    
    can_mine = False
    idx = player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WEAPON)
    if idx != 0:
        item.SelectItem(idx)
        if item.GetItemType() == item.ITEM_TYPE_PICK:
            can_mine = True

    if not can_mine:
        return Action.NEXT_ACTION

    x, y, z = chr.GetPixelPosition(selectedOre)
    if not OpenLib.isPlayerCloseToInstance(selectedOre, 300):
        action_dict = {'function_args': [(x, y)],
                        'function': MoveToPosition,
                        'requirements': {ActionRequirementsCheckers.isNearInstance: [selectedOre]}}
        return action_dict
                    
    if not is_curr_mining and can_mine:
        net.SendOnClickPacket(selectedOre)
        DebugPrint('Digging')
        return False

def ExchangeTrashItemsToEnergyFragments(args):
    from OpenBot.Modules.metin_ui_modules import _Settings as Settings
    first_map = OpenLib.GetPlayerEmpireFirstMap()

    x, y = MapManager.GetNpcFromMap(first_map, 20001)
    return {'function_args': [Settings.instance.sellItems, 20001, (x, y)], # position
            'function': GetEnergyFromAlchemist,
            'on_success': [Action.NEXT_ACTION],
            }

# Demon Tower actions only
def OpenAllSeals(args):
    closest_seal = OpenLib.getClosestInstance([OpenLib.OBJECT_TYPE])
    if closest_seal < 0:
        return True

    slot_with_key = OpenLib.GetItemByID(50084)
    if slot_with_key >= 0:
        chr.SelectInstance(closest_seal)
        action_dict = {'function_args': [chr.GetRace(), slot_with_key], # position
                        'function': UseItemOnNPC,
                        'on_success': [Action.NEXT_ACTION],
                        'on_failed': [Action.NEXT_ACTION],

                        }
        return action_dict
        

    if OpenLib.IsMonsterNearby():
        x, y = args[0]
        #DebugPrint('Clearing the floor')
        action_dict = { 'function_args': [(x, y)], # center position of area 
                        'function': ClearFloor,
                        'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (x, y, 100)},
                        'on_success': [Action.NEXT_ACTION],
                        'interrupt_function': lambda: Action.NEXT_ACTION,
                        'interruptors': [ActionRequirementsCheckers.HasItem],
                        'interruptors_args': [50084]
                    }

        return action_dict
    return Action.NOTHING

def OpenASealInMonument(args):
    center_position = args[0]
    player_x, player_y, player_z = player.GetMainCharacterPosition()
    if not eXLib.FindPath(player_x, player_y, center_position[0], center_position[1]):
        return True

    correct_key = OpenLib.GetItemByID(30304)
    if correct_key >=0:
        monument = OpenLib.getClosestInstance([OpenLib.OBJECT_TYPE])
        chr.SelectInstance(monument)
        action_dict = {'function_args': [chr.GetRace(), correct_key], # position
                        'function': UseItemOnNPC,
                        'on_success': [Action.NEXT_ACTION],
                        'on_failed': [Action.NEXT_ACTION],
                        }
        return action_dict
        
    action_dict = { 'function_args': [(center_position[0], center_position[1])], # center position of area 
                'function': ClearFloor,
                'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (center_position[0], center_position[1])},
                'on_success': [Action.NEXT_ACTION],
                'interrupt_function': lambda: Action.NEXT_ACTION,
                'interruptors': [ActionRequirementsCheckers.HasItem],
                'interruptors_args': [30304]
            }

    return action_dict  

def UpgradeItemInDemonTower(args):
    item_upgrades_list = args[0]
    blacksmith_vid, blacksmith_id = OpenLib.GetBlacksmithFromDemonTower()
    blacksmithX, blacksmithY, blacksmithZ = chr.GetPixelPosition(blacksmith_vid)
    if not OpenLib.isPlayerCloseToPosition(blacksmithX, blacksmithY, 500):
        action_dict = {
            'function_args': [(blacksmithX, blacksmithY)],
            'function': MoveToPosition,
            'requirements': { ActionRequirementsCheckers.IS_ON_POSITION: (blacksmithX, blacksmithY)},
            'on_success': [Action.NEXT_ACTION]
        }
        return action_dict
    
    # Upgrading item
    if item_upgrades_list:
        net.SendRefinePacket(item_upgrades_list.pop(0), 4)
    return Action.NEXT_ACTION
    
def ExitDT(args):
    blacksmith_vid, blacksmith_id = OpenLib.GetBlacksmithFromDemonTower()
    #Creating answer which exit deamon tower
    if player.GetStatus(player.LEVEL) < 75:
        answer = [1, 1, 1]
    else:
        answer = [0, 254, 2]
        action_dict = {
            'function_args': [blacksmith_id, answer, 'metin2_map_deviltower1'],
            'function': TalkWithNPC,
            'on_success': [Action.NEXT_ACTION]
        }
    return action_dict    

def GoToSeventhFloor(args):
    blacksmith_vid, blacksmith_id = OpenLib.GetBlacksmithFromDemonTower()
    if player.GetStatus(player.LEVEL) < 75:
        answer = [1, 1, 1]
    else:
        answer = [0, 254, 2]
    action_dict = {
        'function_args': [blacksmith_id, answer, 'metin2_map_deviltower1'],
        'function': TalkWithNPC,
        'on_success': [Action.NEXT_ACTION]
    }
    return action_dict 

def FindMapInDT(args):
    center_position = args[0]
    correct_map = OpenLib.GetItemByID(30302)
    unknow_old_chest = OpenLib.GetItemByID(30300)
    
    if correct_map >=0:
        net.SendItemUsePacket(correct_map)

    if unknow_old_chest >=0:
        net.SendItemUsePacket(unknow_old_chest)

def WaitFor(args):
    if not len(args) > 1:
        return True
    from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
    modules_to_switch_off = args[1]
    if 'waithack' in modules_to_switch_off:
        waithack_interface.Stop()
    return True

    action_dict = { 'function_args': [(center_position[0], center_position[1])], # center position of area 
                'function': ClearFloor,
                'requirements': {ActionRequirementsCheckers.IS_NEAR_POSITION: (center_position[0], center_position[1])},
                'on_success': [Action.NEXT_ACTION],
                'interruptors_args': [30302, 30300],
                'interruptors': [ActionRequirementsCheckers.HasItem, ActionRequirementsCheckers.HasItem],
                'interrupt_function': lambda: Action.NEXT_ACTION
            }

    return action_dict    
