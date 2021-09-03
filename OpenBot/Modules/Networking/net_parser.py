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
    from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
    #from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
    from OpenBot.Modules.Skillbot.skillbot_ui import skillbot_interface
    hack_status = {
        #'WaitHack': waithack_interface.GetStatus(),
        'FarmBot': farmbot_interface.GetStatus(),
        'SkillBot': skillbot_interface.GetStatus(),
    }

    return hack_status