import os
import shutil
import eXLib
import chat
from OpenBot import simplejson as json
from OpenBot.Modules import OpenLog


PATHS = {
    'SAVES': eXLib.PATH + 'OpenBot/Saves/',
    'PICKUP_LISTS': eXLib.PATH + 'OpenBot/Saves/PickupLists/',
    'SKILLBOT_SETTINGS': eXLib.PATH + 'OpenBot/Saves/SkillbotSettings/',
    'FARMBOT_PATHS': eXLib.PATH + 'OpenBot/Saves/FarmbotPaths/',
    'OTHER_SETTINGS': eXLib.PATH + 'OpenBot/Saves/OtherSettings/',
}
FILENAMES = {
    'PICKUP_FILTER': 'pickup_filter.txt',
    'OTHER_SETTINGS': 'other_settings.txt',
    'FARMBOT_PATH': 'current_path.txt',
}

HACK_STATUS_KEYS = {
    'FISHBOT': 'FishBot',
    'FARMBOT': 'FarmBot',
    'SETTINGS': 'Settings',
    'WAITHACK': 'WaitHack',
    'SKILLBOT': 'SkillBot',
}

STATUS_KEYS = {
    'PICKUP_LISTS': 'PickupLists',
    'FARMBOT_PATHS': 'FarmbotPaths',
    'OTHER_SETTINGS': 'OtherSettings'
}


class FileHandlerInterface:

    def __init__(self):
        self.pickup_lists = []
        self.farmbot_paths = []
        self.other_settings = []

        self._scan_for_pickup_lists()
        self._scan_for_farmbot_paths()
        self._scan_for_others_settings()

    def SetStatus(self, status):
        VALID_STATUS_KEYS = {
            'LOAD_PICKUP_LIST': 'LoadPickupList',
            'LOAD_FARMBOT_PATH': 'LoadFarmbotPath',
            'LOAD_OTHER_SETTINGS': 'LoadOtherSettings',
            'SAVE_PICKUP_LIST': 'SavePickupList',
            'SAVE_FARMBOT_PATH': 'SaveFarmbotPath',
            'SAVE_OTHER_SETTINGS': 'SaveOtherSettings',
            'DELETE_PICKUP_LIST': 'DeletePickupList',
            'DELETE_FARMBOT_PATH': 'DeleteFarmbotPath',
            'DELETE_OTHER_SETTINGS': 'DeleteOtherSettings',
            'RESCAN_PICKUP_LIST': 'RescanPickupList',
            'RESCAN_FARMBOT_PATH': 'RescanFarmbotPath',
            'RESCAN_OTHER_SETTINGS': 'RescanOtherSettings',
        }

        for key in status.keys():

            if VALID_STATUS_KEYS['LOAD_PICKUP_LIST'] == key:
                self.load_pickup_list(status[key])
            elif VALID_STATUS_KEYS['LOAD_FARMBOT_PATH'] == key:
                self.load_farmbot_paths(status[key])
            elif VALID_STATUS_KEYS['LOAD_OTHER_SETTINGS'] == key:
                self.load_other_settings(status[key])

            elif VALID_STATUS_KEYS['SAVE_PICKUP_LIST'] == key:
                self.save_pickup_list(status[key])
            elif VALID_STATUS_KEYS['SAVE_FARMBOT_PATH'] == key:
                self.save_farmbot_paths(status[key])
            elif VALID_STATUS_KEYS['SAVE_OTHER_SETTINGS'] == key:
                self.save_other_settings(status[key])

            elif VALID_STATUS_KEYS['DELETE_PICKUP_LIST'] == key:
                self.del_pickup_list(status[key])
            elif VALID_STATUS_KEYS['DELETE_FARMBOT_PATH'] == key:
                self.del_farmbot_path(status[key])
            elif VALID_STATUS_KEYS['DELETE_OTHER_SETTINGS'] == key:
                self.del_other_settings(status[key])


            elif VALID_STATUS_KEYS['RESCAN_PICKUP_LIST'] == key:
                self._scan_for_pickup_lists()
            elif VALID_STATUS_KEYS['RESCAN_FARMBOT_PATH'] == key:
                self._scan_for_farmbot_paths()
            elif VALID_STATUS_KEYS['RESCAN_OTHER_SETTINGS'] == key:
                self._scan_for_others_settings()

    def GetStatus(self):
        return {
            STATUS_KEYS['PICKUP_LISTS']: [file.replace('.txt', '') for file in self.pickup_lists],
            STATUS_KEYS['FARMBOT_PATHS']: [file.replace('.txt', '') for file in self.farmbot_paths],
            STATUS_KEYS['OTHER_SETTINGS']: [file.replace('.txt', '') for file in self.other_settings],
        }

    @staticmethod
    def __scan_dir_for_files(dir_path):
        return [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]

    def _scan_for_pickup_lists(self):
        self.pickup_lists = self.__scan_dir_for_files(PATHS['PICKUP_LISTS'])

    def _scan_for_farmbot_paths(self):
        self.farmbot_paths = self.__scan_dir_for_files(PATHS['FARMBOT_PATHS'])

    def _scan_for_others_settings(self):
        self.other_settings = self.__scan_dir_for_files(PATHS['OTHER_SETTINGS'])

    def save_pickup_list(self, save_as_filename):
        shutil.copy(PATHS['SAVES'] + FILENAMES['PICKUP_FILTER'], PATHS['PICKUP_LISTS'] + save_as_filename + '.txt')
        self._scan_for_pickup_lists()

    def save_farmbot_paths(self, save_as_filename):
        self.dump_farmbot_path()
        shutil.copy(PATHS['SAVES'] + FILENAMES['FARMBOT_PATH'], PATHS['FARMBOT_PATHS'] + save_as_filename + '.txt')
        self._scan_for_farmbot_paths()

    def save_other_settings(self, save_as_filename):
        self.dump_other_settings()
        shutil.copy(PATHS['SAVES'] + FILENAMES['OTHER_SETTINGS'], PATHS['OTHER_SETTINGS'] + save_as_filename + '.txt')
        self._scan_for_others_settings()

    def del_pickup_list(self, filename):
        self._scan_for_pickup_lists()
        if filename + '.txt' in self.pickup_lists:
            os.remove(PATHS['PICKUP_LISTS'] + filename+ '.txt')
            self._scan_for_pickup_lists()

    def del_farmbot_path(self, filename):
        self._scan_for_farmbot_paths()
        if filename + '.txt' in self.farmbot_paths:
            os.remove(PATHS['FARMBOT_PATHS'] + filename+ '.txt')
            self._scan_for_farmbot_paths()

    def del_other_settings(self, filename):
        self._scan_for_others_settings()
        if filename + '.txt' in self.other_settings:
            os.remove(PATHS['OTHER_SETTINGS'] + filename + '.txt')
            self._scan_for_others_settings()

    def load_pickup_list(self, filename):
        from OpenBot.Modules.Settings.settings_interface import settings_interface

        self._scan_for_pickup_lists()
        if filename + '.txt' in self.pickup_lists:
            with open(PATHS['PICKUP_LISTS'] + filename + '.txt', 'r') as file:
                settings_interface.SetPickupFilter(json.loads(file.read()))

            self.dump_pickup_list()

    @staticmethod
    def load_last_pickup_list():
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        if os.path.isfile(os.path.join(PATHS['SAVES'], FILENAMES['PICKUP_FILTER'])):
            with open(PATHS['SAVES'] + FILENAMES['PICKUP_FILTER'], 'r') as file:
                settings_interface.SetPickupFilter(json.loads(file.read()))

    def load_farmbot_paths(self, filename):
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        self._scan_for_farmbot_paths()
        if filename + '.txt' in self.farmbot_paths:
            with open(PATHS['FARMBOT_PATHS'] + filename + '.txt', 'r') as file:
                status = farmbot_interface.GetStatus()
                status['Path'] = json.loads(file.read())
                farmbot_interface.SetStatus(status)

            self.dump_farmbot_path()

    @staticmethod
    def load_last_farmbot_paths():
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        if os.path.isfile(os.path.join(PATHS['SAVES'], FILENAMES['FARMBOT_PATH'])):
            with open(PATHS['SAVES'] + FILENAMES['FARMBOT_PATH'], 'r') as file:
                path = json.loads(file.read())
                farmbot_interface.SetStatus({'Path': path})

    def load_other_settings(self, filename):
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        from OpenBot.Modules.Fishbot.fishbot_interface import fishbot_interface
        from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
        from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface

        self._scan_for_others_settings()
        if filename + '.txt' in self.other_settings:
            with open(PATHS['OTHER_SETTINGS'] + filename + '.txt', 'r') as file:
                other_settings = json.loads(file.read())
                for status in other_settings.keys():
                    if HACK_STATUS_KEYS['FARMBOT'] == status:
                        farmbot_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['FARMBOT']), save_status=False)
                    elif HACK_STATUS_KEYS['SETTINGS'] == status:
                        settings_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['SETTINGS']), save_status=False)
                    elif HACK_STATUS_KEYS['FISHBOT'] == status:
                        fishbot_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['FISHBOT']), save_status=False)
                    elif HACK_STATUS_KEYS['WAITHACK'] == status:
                        waithack_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['WAITHACK']), save_status=False)
                    elif HACK_STATUS_KEYS['SKILLBOT'] == status:
                        skillbot_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['SKILLBOT']), save_status=False)

    def load_last_other_settings(self):
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        from OpenBot.Modules.Fishbot.fishbot_interface import fishbot_interface
        from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
        from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface

        if os.path.isfile(os.path.join(PATHS['SAVES'], FILENAMES['OTHER_SETTINGS'])):
            with open(PATHS['SAVES'] + FILENAMES['OTHER_SETTINGS'], 'r') as file:
                other_settings = json.loads(file.read())
                for status in other_settings.keys():

                    if HACK_STATUS_KEYS['FARMBOT'] == status:
                        new_status = self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['FARMBOT'])
                        farmbot_interface.SetStatus(new_status, save_status=False)
                    elif HACK_STATUS_KEYS['SETTINGS'] == status:
                        settings_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['SETTINGS']), save_status=False)
                    elif HACK_STATUS_KEYS['FISHBOT'] == status:
                        fishbot_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['FISHBOT']), save_status=False)
                    elif HACK_STATUS_KEYS['WAITHACK'] == status:
                        waithack_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['WAITHACK']), save_status=False)
                    elif HACK_STATUS_KEYS['SKILLBOT'] == status:
                        skillbot_interface.SetStatus(self.return_dict_with_diff(other_settings[status], HACK_STATUS_KEYS['SKILLBOT']), save_status=False)

    def return_dict_with_diff(self, new_status, status):
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        from OpenBot.Modules.Fishbot.fishbot_interface import fishbot_interface
        from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
        from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface

        diff_dict = {}
        if HACK_STATUS_KEYS['FARMBOT'] == status:
            old_status = farmbot_interface.GetStatus()
        elif HACK_STATUS_KEYS['SETTINGS'] == status:
            old_status = settings_interface.GetStatus()
        elif HACK_STATUS_KEYS['FISHBOT'] == status:
            old_status = fishbot_interface.GetStatus()
        elif HACK_STATUS_KEYS['WAITHACK'] == status:
            old_status = waithack_interface.GetStatus()
        elif HACK_STATUS_KEYS['SKILLBOT'] == status:
            old_status = skillbot_interface.GetStatus()


        for key in old_status.keys():
            if new_status[key] != old_status[key]:
                diff_dict[key] = new_status[key]
        return diff_dict

    def load_last_skills(self):
        from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface
        if os.path.isfile(os.path.join(PATHS['SAVES'], FILENAMES['OTHER_SETTINGS'])):
            with open(PATHS['SAVES'] + FILENAMES['OTHER_SETTINGS'], 'r') as file:
                other_settings = json.loads(file.read())
                for status in other_settings.keys():

                    if HACK_STATUS_KEYS['SKILLBOT'] == status:
                        skillbot_interface.SetStatus({'CurrentSkillSet': other_settings[status]['CurrentSkillSet']}, save_status=False)

    @staticmethod
    def dump_pickup_list():
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        pickup_filter = settings_interface.ReturnPickupFilter()
        with open(PATHS['SAVES'] + FILENAMES['PICKUP_FILTER'], 'w') as file:
            file.write(json.dumps(pickup_filter))

    @staticmethod
    def dump_farmbot_path():
        from OpenBot.Modules.Farmbot import farmbot_interface
        path = farmbot_interface.farmbot_interface.GetStatus()['Path']
        with open(PATHS['SAVES'] + FILENAMES['FARMBOT_PATH'], 'w') as file:
            file.write(json.dumps(path))                                                                                                                                                                                                                                                         

    @staticmethod
    def dump_other_settings():
        from OpenBot.Modules.Settings.settings_interface import settings_interface
        from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
        from OpenBot.Modules.Fishbot.fishbot_interface import fishbot_interface
        from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
        from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface

        other_settings = {
            HACK_STATUS_KEYS['FISHBOT']: fishbot_interface.GetStatus(),
            HACK_STATUS_KEYS['FARMBOT']: farmbot_interface.GetStatus(),
            HACK_STATUS_KEYS['SETTINGS']: settings_interface.GetStatus(),
            HACK_STATUS_KEYS['WAITHACK']: waithack_interface.GetStatus(),
            HACK_STATUS_KEYS['SKILLBOT']: skillbot_interface.GetStatus()
        }

        other_settings[HACK_STATUS_KEYS['WAITHACK']]['Enabled'] = False
        other_settings[HACK_STATUS_KEYS['FARMBOT']]['Enabled'] = False
        other_settings[HACK_STATUS_KEYS['SETTINGS']]['RenderTextures'] = True
        other_settings[HACK_STATUS_KEYS['FISHBOT']]['Enabled'] = False

        with open(PATHS['SAVES'] + 'other_settings.txt', 'w') as file:
            file.write(json.dumps(other_settings, indent=4))


file_handler_interface = FileHandlerInterface()

