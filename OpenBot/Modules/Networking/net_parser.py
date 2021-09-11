import eXLib
import chr, app, item
from OpenBot.Modules import OpenLib, OpenLog
from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
from OpenBot.Modules.Waithack.waithack_interface import waithack_interface
from OpenBot.Modules.Skillbot.skillbot_ui import skillbot_interface
from OpenBot.Modules.Settings.settings_interface import settings_interface
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface

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

def parse_all_items_in_database():
    all_items = []
    try:
        lines = open(app.GetLocalePath()+"/item_list.txt", "r").readlines()
    except IOError:
        OpenLog.DebugPrint("Load Itemlist Error, you have to set the IDs manually")
        return all_items
    for line in lines:
        tokens = str(line).split("\t")
        Index = str(tokens[0])
        try:
            Itemname = item.GetItemName(item.SelectItem(int(Index)))
        except Exception:
            continue
        all_items.append({
            'id': Index,
            'name': Itemname,
        })
    return all_items

def parse_character_status_info():
    status = OpenLib.getAllStatusOfMainActor()
    #OpenLog.DebugPrint(str(status))
    return status

def parse_hack_status():
    hack_status = {
        'Settings': settings_interface.GetStatus(),
        'WaitHack': waithack_interface.GetStatus(),
        'FarmBot': farmbot_interface.GetStatus(),
        'SkillBot': skillbot_interface.GetStatus(),
        'ActionBot': action_bot_interface.GetStatus(),
    }

    return hack_status