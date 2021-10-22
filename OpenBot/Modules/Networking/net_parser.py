import eXLib
import chr, app, item, player
from OpenBot.Modules import OpenLib, OpenLog
import codecs

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

def parse_channel_switcher_status():
    from OpenBot.Modules.ChannelSwitcher.channel_switcher_interface import channel_switcher_interface
    hack_status = {
        'ChannelSwitcher': channel_switcher_interface.GetStatus()
    }
    return hack_status

def parse_inventory_status():
    from OpenBot.Modules.Inventory.inventory_interface import inventory_interface
    return inventory_interface.GetStatus()

def parse_pickup_filter():
    from OpenBot.Modules.Settings.settings_interface import settings_interface
    return settings_interface.GetPickupFilter()

#####
# Converting to UTF 8 Methods
# ignoring ints, floats and other numbers in this conversion. only texts of values relevant.

def convertToUTF8(data,enc='cp1252'):
    if (isinstance(data,dict)):
        return dictToUtf8(data,enc)
    elif (isinstance(data,tuple)):
        return tupleToUtf8(data,enc)
    elif (isinstance(data,list)):
        return listToUtf8(data,enc)
    elif (isinstance(data,str)):
        return stringToUTF8(data,enc)
    return data

def dictToUtf8(dic,enc):
    for key in dic:
        if (isinstance(dic[key],dict)):
            dic[key] = dictToUtf8(dic[key],enc)
        elif (isinstance(dic[key],tuple)):
            dic[key] = tupleToUtf8(dic[key],enc)
        elif (isinstance(dic[key],list)):
            dic[key] = listToUtf8(dic[key],enc)
        elif (isinstance(dic[key],str)):
            dic[key] = stringToUTF8(dic[key],enc)
    return dic
def tupleToUtf8(tupl,enc):
    tupl_new=[]
    for item in tupl:
        if(isinstance(item,str)):
            item=stringToUTF8(item,enc)
        elif(isinstance(item,dict)):
            item=dictToUtf8(item,enc)
        elif(isinstance(item,list)):
            item=listToUtf8(item,enc)
        elif(isinstance(item,tuple)):
            item=tupleToUtf8(item,enc)
        tupl_new.append(item)
    return tuple(tupl_new)
def listToUtf8(lis,enc):
    lis_new=[]
    for item in lis:
        if(isinstance(item,str)):
            item=stringToUTF8(item,enc)
        elif(isinstance(item,dict)):
            item=dictToUtf8(item,enc)
        elif(isinstance(item,list)):
            item=listToUtf8(item,enc)
        elif(isinstance(item,tuple)):
            item=tupleToUtf8(item,enc)
        lis_new.append(item)
    return lis_new
    
def stringToUTF8(s, enc):
    s = codecs.decode(s, encoding=str(enc))
    return s