from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Farmbot.farmbot_module import farm as farm_instance


class FarmbotInterface:

    def __init__(self):
        pass

    def SetStatus(self, status):
        good_keys = ['Enabled', 'CurrentWaypointIndex', 'Path','OresToMine','WaitingTime','ChangeChannel','LookForMetins', 'LookForOre', 'ExchangeItemsToEnergy']
        if not type(status) == dict:
            return False
        
        for key in status.keys():
            if key not in good_keys:
                return False
        
        if status['Enabled']:
            self.Start()
        else:
            self.Stop()

        farm_instance.path = status['Path']
        farm_instance.switch_channels = status['ChangeChannel']
        farm_instance.look_for_metins = status['LookForMetins']
        farm_instance.look_for_ore = status['LookForOre']
        farm_instance.ores_to_mine = status['OresToMine']
        farm_instance.exchange_items_to_energy = status['ExchangeItemsToEnergy']

    def GetStatus(self):
        return {
            'Enabled': farm_instance.enabled,
            'CurrentWaypointIndex': farm_instance.current_point,
            'Path': farm_instance.path,
            'OresToMine': farm_instance.ores_to_mine,
            'WaitingTime': farm_instance.timeForWaitingState,
            'ChangeChannel': farm_instance.switch_channels,
            'LookForMetins': farm_instance.look_for_metins,
            'LookForOre': farm_instance.look_for_ore,
            'ExchangeItemsToEnergy': farm_instance.exchange_items_to_energy
        }

    def IsOn(self):
        DebugPrint('Farmbot is enabled ' + str(farm_instance.enabled))
        return farm_instance.enabled

    def Start(self):
        return farm_instance.onStart()

    def Stop(self):
        return farm_instance.onStop()

    def AddPoint(self, point):
        if type(point) != dict:
            return False
        for key in point.keys():
            if key not in ['x', 'y', 'map_name']:
                return False
        farm_instance.add_point(point)
        return True
    
    def RemovePoint(self, point):
        if type(point) != dict:
            return False
        for key in point.keys():
            if key not in ['x', 'y', 'map_name']:
                return False 
        farm_instance.delete_point(point)

    def ClearPath(self):
        farm_instance.path = []

    def AddOreToMine(self, ore_id):
        if not type(ore_id) == int:
            return False
        if ore_id in farm_instance.ores_to_mine:
            return True
        farm_instance.ores_to_mine.append(ore_id)
        return True
    
    def RemoveOreToMine(self, ore_id):
        if not type(ore_id) == int:
            return False
        if ore_id in farm_instance.ores_to_mine:
            farm_instance.ores_to_mine.remove(ore_id)
            return True
        return False

    def SavePath(self, filename):
        if not type(filename) == str:
            return False
        return farm_instance.save_path(filename)
    
    def LoadPath(self, filename):
        if not type(filename) == str:
            return False
        return farm_instance.load_path(filename)

    def SetWaitingTime(self, waiting_time):
        if not type(waiting_time) == int or not type(waiting_time) == float:
            return False
        DebugPrint('waiting_time is now ' + str(farm_instance.waiting_time))
        farm_instance.timeForWaitingState = waiting_time

    def SwitchChangeChannel(self, val=None):
        if farm_instance.switch_channels:
            farm_instance.switch_channels = False
        else:
            farm_instance.switch_channels = True
        DebugPrint('switch_channels is now ' + str(farm_instance.switch_channels))
        return farm_instance.switch_channels

    def SwitchLookForMetins(self, val=None):
        if farm_instance.look_for_metins:
            farm_instance.look_for_metins = False
        else:
            farm_instance.look_for_metins = True
            if farm_instance.look_for_ore:
                self.SwitchLookForOre()
        DebugPrint('look_for_metins is now ' + str(farm_instance.look_for_metins))
        return farm_instance.look_for_metins

    def SwitchLookForOre(self, val=None):
        if farm_instance.look_for_ore:
            farm_instance.look_for_ore = False
        else:
            farm_instance.look_for_ore = True
            if farm_instance.look_for_metins:
                self.SwitchLookForMetins()
        DebugPrint('LookForOre is now ' + str(farm_instance.look_for_ore))
        return farm_instance.look_for_ore


    def SwitchExchangeItemsToEnergy(self, val=None):
        if farm_instance.exchange_items_to_energy:
            farm_instance.exchange_items_to_energy = False
        else:
            farm_instance.exchange_items_to_energy = True
        DebugPrint('exchange_items_to_energy is now ' + str(farm_instance.exchange_items_to_energy))
        return farm_instance.exchange_items_to_energy

farmbot_interface = FarmbotInterface()