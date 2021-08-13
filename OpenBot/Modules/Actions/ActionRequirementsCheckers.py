from OpenBot.Modules import OpenLib
from OpenBot.Modules.OpenLog import DebugPrint
import eXLib
import player, background, chat, chr

# REQUIREMENTS
IS_NEAR_POSITION = 'isNearPosition'
IS_ON_POSITION = 'isOnPosition'
IS_IN_MAP = 'isInMap'
IS_ABOVE_LVL = 'isAboveLvl'
IS_NEAR_INSTANCE = 'inNearInstance'
IS_RACE_NEARLY = 'isRaceNearly'

def isAboveLVL(lvl):
    """
     Checking is main character above level
        Args:
            lvl (int)

    """
    
    
    if player.GetStatus(player.LEVEL) < lvl:
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

def isNearInstance(vid):
    return OpenLib.isPlayerCloseToInstance(vid)

def isNearPosition(position):
    """
        Checking is main character near position.
        Args:
            position [x (int), y(int), max_dist(int)](list)

    """
    x, y = position[0], position[1]
    if len(position) < 3:
        max_dist = 100
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
        max_dist = 100
    else:
        max_dist = position[2]
    if OpenLib.isPlayerCloseToPosition(x, y, max_dist):
        DebugPrint('player on pos')
        return True
    DebugPrint('player not on pos')
    return False

def isMetinNearly(args=0):
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
            DebugPrint('there is metin!')
            return True
    return False

def isOreNearly(args=0):
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisOre(vid):
            return True
    return False

def isRaceNearly(races_list):
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        if chr.GetRace() in races_list:
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