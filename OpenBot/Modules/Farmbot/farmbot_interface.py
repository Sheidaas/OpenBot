from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Farmbot.farmbot_module import farm as farm_instance


STATUS_KEYS = {
    'CURRENT_POINT': 'CurrentPoint',
    'PATH': 'Path',
    'ENABLED': 'Enabled',
    'ORES_TO_MINE': 'OresToMine',
    'WAITING_TIME': 'WaitingTime',
    'CHANGE_CHANNELS': 'ChangeChannels',
    'LOOK_FOR_METINS': 'LookForMetins',
    'LOOK_FOR_ORE': 'LookForOre',
    'EXCHANGE_ITEMS_TO_ENERGY': 'ExchangeItemsToEnergy',
    'CLEAR_PATH': 'ClearPath'
}


class FarmbotInterface:

    def __init__(self):
        pass

    def SetStatus(self, status, save_status=True):

        for status_key in status.keys():
            if STATUS_KEYS['PATH'] == status_key:
                self.CreatePath(status[status_key])

            elif STATUS_KEYS['ENABLED'] == status_key:
                self.SwitchEnabled()

            elif STATUS_KEYS['ORES_TO_MINE'] == status_key:
                farm_instance.ores_to_mine = []
                for ore_id in status['OresToMine']:
                    self.AddOreToMine(ore_id)

            elif STATUS_KEYS['CHANGE_CHANNELS'] == status_key:
                self.SwitchChangeChannel()

            elif STATUS_KEYS['LOOK_FOR_METINS'] == status_key:
                self.SwitchLookForMetins()

            elif STATUS_KEYS['LOOK_FOR_ORE'] == status_key:
                self.SwitchLookForOre()

            elif STATUS_KEYS['EXCHANGE_ITEMS_TO_ENERGY'] == status_key:
                self.SwitchExchangeItemsToEnergy()

            elif STATUS_KEYS['WAITING_TIME'] == status_key:
                self.SetWaitingTime(status[status_key])

            elif STATUS_KEYS['CLEAR_PATH'] == status_key:
                self.ClearPath()
        
        if save_status: self.SaveStatus()

    def GetStatus(self):
        return{
            STATUS_KEYS['ENABLED']: farm_instance.enabled,
            STATUS_KEYS['CURRENT_POINT']: farm_instance.current_point,
            STATUS_KEYS['PATH']: farm_instance.path,
            STATUS_KEYS['ORES_TO_MINE']: farm_instance.ores_to_mine,
            STATUS_KEYS['WAITING_TIME']: farm_instance.timeForWaitingState,
            STATUS_KEYS['CHANGE_CHANNELS']: farm_instance.switch_channels,
            STATUS_KEYS['LOOK_FOR_METINS']: farm_instance.look_for_metins,
            STATUS_KEYS['LOOK_FOR_ORE']: farm_instance.look_for_ore,
            STATUS_KEYS['EXCHANGE_ITEMS_TO_ENERGY']: farm_instance.exchange_items_to_energy
        }

    def SaveStatus(self):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        file_handler_interface.dump_other_settings()

    def IsOn(self):
        return farm_instance.enabled

    def SwitchEnabled(self):
        if farm_instance.enabled:
            self.Stop()
        else:
            self.Start()

    def Start(self):
        return farm_instance.onStart()

    def Stop(self):
        return farm_instance.onStop()

    def CreatePath(self, path):
        farm_instance.path = []
        for point in path:
            self.AddPoint({
                'x': point[0],
                'y': point[1],
                'map_name': str(point[2])
            })

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
        farm_instance.timeForWaitingState = waiting_time

    def SwitchChangeChannel(self, val=None):
        if farm_instance.switch_channels:
            farm_instance.switch_channels = False
        else:
            farm_instance.switch_channels = True
        return farm_instance.switch_channels

    def SwitchLookForMetins(self, val=None):
        if farm_instance.look_for_metins:
            farm_instance.look_for_metins = False
        else:
            farm_instance.look_for_metins = True
            if farm_instance.look_for_ore:
                self.SwitchLookForOre()
        return farm_instance.look_for_metins

    def SwitchLookForOre(self, val=None):
        if farm_instance.look_for_ore:
            farm_instance.look_for_ore = False
        else:
            farm_instance.look_for_ore = True
            if farm_instance.look_for_metins:
                self.SwitchLookForMetins()
        return farm_instance.look_for_ore


    def SwitchExchangeItemsToEnergy(self, val=None):
        if farm_instance.exchange_items_to_energy:
            farm_instance.exchange_items_to_energy = False
        else:
            farm_instance.exchange_items_to_energy = True
        return farm_instance.exchange_items_to_energy

farmbot_interface = FarmbotInterface()