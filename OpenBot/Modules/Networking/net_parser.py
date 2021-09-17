import eXLib
import chr, app, item, player
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

def parse_static_character_status_info():
    status = OpenLib.getAllStatusOfMainActor()
    return {
        'Server': status['Server'],
        'Name': status['Name'],
        'FirstEmpireMap': status['FirstEmpireMap'],
    }

def parse_character_status_info():
    status = OpenLib.getAllStatusOfMainActor()
    #OpenLog.DebugPrint(str(status))
    return status

def parse_skill_bot_status():
    from OpenBot.Modules.Skillbot.skillbot_ui import skillbot_interface
    hack_status = {
        'SkillBot': skillbot_interface.GetStatus(),
    }
    return hack_status

def parse_action_bot_status():
    from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
    hack_status = {
        'ActionBot': action_bot_interface.GetStatus(),
    }
    return hack_status

def parse_wait_hack_status():
    from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
    hack_status = {
        'WaitHack': waithack_interface.GetStatus(),
    }
    return hack_status

def parse_settings_status():
    from OpenBot.Modules.Settings.settings_interface import settings_interface
    hack_status = {
        'Settings': settings_interface.GetStatus(),
    }
    return hack_status

def parse_farm_bot_status():
    from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
    hack_status = {
        'FarmBot': farmbot_interface.GetStatus(),
    }
    return hack_status

def parse_inventory_status():
    from OpenBot.Modules.Inventory.inventory_interface import inventory_interface
    return inventory_interface.GetStatus()

def parse_pickup_filter():
    from OpenBot.Modules.Settings.settings_interface import settings_interface
    return settings_interface.GetPickupFilter()