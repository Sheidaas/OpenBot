import eXLib
import chr
from OpenBot.Modules import OpenLib, OpenLog

def parse_instances_list():
    instances_list = [None] * len(eXLib.InstancesList)
    for i,vid in enumerate(eXLib.InstancesList):
        chr.SelectInstance(vid)
        x, y, z = chr.GetPixelPosition(vid)
        _id = chr.GetRace()
        _type = chr.GetInstanceType(vid)
        instances_list[i] = {
            'vid': vid,
            'id': _id,
            'x': x,
            'y': y,
            'type': _type
        }
    return instances_list

def parse_character_status_info():
    status = OpenLib.getAllStatusOfMainActor()
    #OpenLog.DebugPrint(str(status))
    return status

def parse_hack_status():
    from OpenBot.Modules import DmgHacks
    from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
    hack_status = {
        'WaitHack': {
            'enable': DmgHacks.Dmg.enableButton.isOn,
            'switches': {
                'IsWallBetween': DmgHacks.Dmg.wallBtn.isOn,
                'CheckIsPlayer': DmgHacks.Dmg.playerClose.isOn,
                'CloudExploit': DmgHacks.Dmg.cloudBtn.isOn,
                'AttackBlockedMonsters': DmgHacks.Dmg.attackBlockedMonsters.isOn,
                'AttackPlayers': DmgHacks.Dmg.attackPlayerBtn.isOn,
            },
            'values': {
                'Range': DmgHacks.Dmg.range,
                'Monsters': DmgHacks.Dmg.maxMonster,
                'Speed': DmgHacks.Dmg.speed * 1000,
            }
        },
        'FarmBot': farmbot_interface.GetStatus()
    }

    return hack_status