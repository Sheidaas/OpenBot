from OpenBot.Modules import OpenLib
from OpenBot.Modules.OpenLog import DebugPrint
import eXLib
import player, background, chat, chr, net

# REQUIREMENTS
IS_NEAR_POSITION = 'IS_NEAR_POSITION'
IS_ON_POSITION = 'IS_ON_POSITION'
IS_IN_MAP = 'IS_IN_MAP'
IS_ABOVE_LVL = 'IS_ABOVE_LVL'
IS_UNDER_LVL = 'IS_UNDER_LVL'
IS_NEAR_INSTANCE = 'IS_NEAR_INSTANCE'
IS_RACE_NEARLY = 'IS_RACE_NEARLY'
IS_IN_CHANNEL = 'IS_IN_CHANNEL'
IS_CHAR_READY_TO_MINE = 'IS_CHAR_READY_TO_MINE'
IS_DEAD = 'IS_DEAD'
IS_HP_RECOVERED = 'IS_HP_RECOVERED'
HAS_ITEM = 'HAS_ITEM'
HAS_ITEM_IN_COUNT = 'HAS_ITEM_IN_COUNT'
IS_INVENTORY_FULL = 'IS_INVENTORY_FULL'


req_list = [IS_NEAR_POSITION, IS_ON_POSITION, IS_IN_MAP, IS_ABOVE_LVL, IS_NEAR_INSTANCE, IS_RACE_NEARLY, IS_IN_CHANNEL, IS_DEAD, HAS_ITEM, HAS_ITEM_IN_COUNT, IS_INVENTORY_FULL]
interrupt_list = [IS_NEAR_POSITION, IS_ON_POSITION, IS_IN_MAP, IS_ABOVE_LVL, IS_NEAR_INSTANCE, IS_RACE_NEARLY, IS_IN_CHANNEL, IS_DEAD, HAS_ITEM, HAS_ITEM_IN_COUNT, IS_INVENTORY_FULL]


def isAboveLVL(lvl):
    """
     Checking is main character above level
        Args:
            lvl (int)

    """
    
    
    if player.GetStatus(player.LEVEL) < lvl:
        return False
    return True

def isUnderLVL(lvl):
    if player.GetStatus(player.LEVEL) > lvl:
        return False
    return True   

def isInMaps(maps):
    """
        Checking is main character on any of map in list
        Args:
            maps ['map_name_1' (str), 'map_name_2' (str)] (list)

    """
    for mapName in maps:
        if str(background.GetCurrentMapName()) == mapName:
            return True
    return False

def isNearInstance(vid, max_dist=250):
    return OpenLib.isPlayerCloseToInstance(vid, max_dist)

def isNearPosition(position):
    """
        Checking is main character near position.
        Args:
            position [x (int), y(int), max_dist(int)](list)

    """
    x, y = position[0], position[1]
    if len(position) < 3:
        max_dist = 150
    else:
        max_dist = position[2]
    return OpenLib.isPlayerCloseToPosition(x, y, max_dist)

def isOnPosition(position):
    """
        Checking is main character on current position.
        Args:
            position [x (int), y(int), max_dist(int)](list)

    """
    x, y = position[0], position[1]
    if len(position) < 3:
        max_dist = 200
    else:
        max_dist = position[2]
    if OpenLib.isPlayerCloseToPosition(x, y, max_dist):
        return True
    return False

def isMetinNearly(skipped_list):
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
            if not OpenLib.isPathToVID(vid):
                continue
            if OpenLib.isVidBlocked(vid):
                continue
            if vid in skipped_list:
                continue
            return True
    return False

def IsVidNotExist(selected_vid):
    for vid in eXLib.InstancesList:
        if vid == selected_vid:
            return False
    return True

def areItemsNearly(items):
    x1, y1, z1 = chr.GetPixelPosition(net.GetMainActorVID())
    for item in items:
        if OpenLib.dist(x1, y1, item['position'][0], item['position'][1]) <= 2000:
            return True
    return False

def isOreNearly(args=0):
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisOre(vid) and not eXLib.IsDead(vid):
            if not OpenLib.isPathToVID(vid):
                continue
            return True
    return False

def isRaceNearly(args):
    my_x, my_y, my_z = chr.GetPixelPosition(net.GetMainActorVID())
    races_list = args[0]
    skipped_vids = args[1]
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if vid in skipped_vids:
            continue
        if eXLib.IsDead(vid):
            continue

        x2, y2, z2 = chr.GetPixelPosition(vid)
        if chr.GetRace(vid) in races_list and OpenLib.dist(my_x, my_y, x2, y2) <= 10000:
            return True
    return False

def isRaceNearlyFromExactPoint(args):
    x, y = args[0]
    races_list = args[0]
    skipped_vids = args[1]
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if vid in skipped_vids:
            continue
        x2, y2, z2 = chr.GetPixelPosition(vid)
        if chr.GetRace(vid) in races_list and OpenLib.dist(x, y, x2, y2) <= 10000:
            return True
    return False

def isVidNearly(vid):
    if player.GetCharacterDistance(vid) < OpenLib.ATTACK_RANGE:
        return True
    return False

def isCharReadyToMine(ore_vid):

    if eXLib.IsDead(ore_vid):
        return False

    if not OpenLib.isPlayerCloseToInstance(ore_vid):
        return False
    
    if not OpenLib.IsWeaponPickaxe():
        return False

    return True

def HasItem(item_id):
    if OpenLib.GetItemByID(item_id) > -1:
        return True
    return False

def HasItemInCount(item_id, item_count):
    item_slot = OpenLib.GetItemByID(item_id)
    if item_slot > -1:
        if player.GetItemCount(item_slot) >= item_count:
            return True
        return False
    return False

def IsDead(vid):
    return eXLib.IsDead(vid)

def IsInChannel(channel):
    if OpenLib.GetCurrentChannel() == channel:
        return True
    return False

def IsHPRecovered(args):
    if float(player.GetStatus(player.HP)) / float(player.GetStatus(player.MAX_HP)) * 100 >= 50:
        return True
    return False 

def isInventoryFull(args=0):
    return OpenLib.isInventoryFull()

def ActorDistanceToVidSmallerThan(args):
    target = args[0]
    distance = args[1]
    my_x, my_y, z = chr.GetPixelPosition(net.GetMainActorVID())
    target_x, target_y, z = chr.GetPixelPosition(target)
    if distance >= OpenLib.dist(my_x, my_y, target_x, target_y):
        return True
    return False

def IsMobCloserThan(distance):
    my_x, my_y, z = chr.GetPixelPosition(net.GetMainActorVID())
    for vid in eXLib.InstancesList:
        if vid == net.GetMainActorVID():
            continue

        if chr.GetInstanceType(vid) != OpenLib.MONSTER_TYPE:
            continue

        target_x, target_y, z = chr.GetPixelPosition(vid)

        if distance >= OpenLib.dist(my_x, my_y, target_x, target_y):
            return True
    return False



