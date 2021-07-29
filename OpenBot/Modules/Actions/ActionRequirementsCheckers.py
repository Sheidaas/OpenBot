from OpenBot.Modules import OpenLib
from OpenBot.Modules.OpenLog import DebugPrint
import eXLib
import player, background, chat

# REQUIREMENTS
IS_NEAR_POSITION = 'isNearPosition'
IS_ON_POSITION = 'isOnPosition'
IS_IN_MAP = 'isInMap'
IS_ABOVE_LVL = 'isAboveLvl'

def isAboveLVL(lvl):
    """
     Checking is main character above level
        Args:
            lvl (int)

    """
    
    
    #if int(player.LEVEL_TYPE_BASE) < lvl:
    #    return False
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

def isMetinNearly():
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
            return True
    return False

def isOreNearly():
    for vid in eXLib.InstancesList:
        if OpenLib.IsThisOre(vid):
            return True
    return False