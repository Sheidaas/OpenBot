from OpenBot.Modules.Settings.settings_module import instance
import app

STATUS_KEYS = {
    'PICKUP_RANGE': 'PickupRange',
    'RESTART_HERE': 'RestartHere',
    'RESTART_IN_CITY': 'RestartInCity',
    'BLUE_POTIONS': 'BluePotions',
    'MIN_MANA': 'MinMana',
    'RED_POTIONS': 'RedPotions',
    'MIN_HEALTH': 'MinHealth',
    'SPEEDHACK': 'Speedhack',
    'ANTI_EXP': 'AntiExp',
    'SPEED_MULTIPLIER': 'SpeedMultiplier',
    'PICKUP': 'Pickup',
    'PICKUP_SPEED': 'PickupSpeed',
    'EXCLUDE_IN_FILTER': 'ExcludeInFilter',
    'USE_RANGE_PICKUP': 'UseRangePickup',
    'AVOID_PLAYERS_IN_PICKUP': 'AvoidPlayersInPickup',
    'USE_WALLHACK': 'UseWallhack',
    'AUTO_LOGIN': 'AutoLogin',
    'PICKUP_ITEM_FIRST': 'PickupItemFirst',
    'PICKUP_IGNORE_PATH': 'PickupIgnorePath',
    'RENDER_TEXTURES': 'RenderTextures',
    'EXIT_METIN': 'ExitMetin',
}

class SettingsInterface:

    def SetStatus(self, status, save_status=True):

        for status_key in status.keys():
            if STATUS_KEYS['PICKUP_RANGE'] == status_key:
                self.SetPickupRange(status[status_key])

            elif STATUS_KEYS['RESTART_HERE'] == status_key:
                self.SwitchRestartHere()

            elif STATUS_KEYS['RESTART_IN_CITY'] == status_key:
                self.SwitchRestartInCity()

            elif STATUS_KEYS['BLUE_POTIONS'] == status_key:
                self.SwitchBluePotions()

            elif STATUS_KEYS['MIN_MANA'] == status_key:
                self.SetMinMana(status[status_key])

            elif STATUS_KEYS['RED_POTIONS'] == status_key:
                self.SwitchRedPotions()

            elif STATUS_KEYS['MIN_HEALTH'] == status_key:
                self.SetMinHealth(status[status_key])

            elif STATUS_KEYS['SPEEDHACK'] == status_key:
                self.SwitchSpeedHack()

            elif STATUS_KEYS['ANTI_EXP'] == status_key:
                self.SwitchAntiExp()

            elif STATUS_KEYS['SPEED_MULTIPLIER'] == status_key:
                self.SetSpeedMultiplier(status[status_key])

            elif STATUS_KEYS['PICKUP'] == status_key:
                self.SwitchPickup()

            elif STATUS_KEYS['PICKUP_SPEED'] == status_key:
                self.SetPickupSpeed(status[status_key])

            elif STATUS_KEYS['EXCLUDE_IN_FILTER'] == status_key:
                self.SwitchExcludeInFilter()

            elif STATUS_KEYS['USE_RANGE_PICKUP'] == status_key:
                self.SwitchUseRangePickup()

            elif STATUS_KEYS['AVOID_PLAYERS_IN_PICKUP'] == status_key:
                self.SwitchAvoidPlayersInPickup()

            elif STATUS_KEYS['USE_WALLHACK'] == status_key:
                self.SwitchWallhack()

            elif STATUS_KEYS['AUTO_LOGIN'] == status_key:
                self.SwitchAutoLogin()

            elif STATUS_KEYS['PICKUP_ITEM_FIRST'] == status_key:
                self.SwitchPickupItemFirst()

            elif STATUS_KEYS['PICKUP_IGNORE_PATH'] == status_key:
                self.SwitchPickupIgnorePath()

            elif STATUS_KEYS['RENDER_TEXTURES'] == status_key:
                instance.switch_render_textures()

            elif STATUS_KEYS['EXIT_METIN'] == status_key:
                app.Abort()

        if save_status: self.SaveStatus()

    def GetStatus(self):
        return {
            STATUS_KEYS['RENDER_TEXTURES']: instance.renderTextures,
            STATUS_KEYS['RESTART_HERE']: instance.restartHere,
            STATUS_KEYS['RESTART_IN_CITY']: instance.restartInCity,
            STATUS_KEYS['BLUE_POTIONS']: instance.bluePotions,
            STATUS_KEYS['MIN_MANA']: instance.minMana,
            STATUS_KEYS['RED_POTIONS']: instance.redPotions,
            STATUS_KEYS['MIN_HEALTH']: instance.minHealth,
            STATUS_KEYS['SPEEDHACK']: instance.speedHack,
            STATUS_KEYS['ANTI_EXP']: instance.antiExp,
            STATUS_KEYS['SPEED_MULTIPLIER']: instance.speedMultiplier,
            STATUS_KEYS['PICKUP']: instance.pickUp,
            STATUS_KEYS['PICKUP_RANGE']: instance.pickUpRange,
            STATUS_KEYS['PICKUP_SPEED']: instance.pickUpSpeed,
            STATUS_KEYS['EXCLUDE_IN_FILTER']: instance.excludeInFilter,
            STATUS_KEYS['USE_RANGE_PICKUP']: instance.useRangePickup,
            STATUS_KEYS['AVOID_PLAYERS_IN_PICKUP']: instance.doNotPickupIfPlayerHere,
            STATUS_KEYS['PICKUP_ITEM_FIRST']: instance.pickItemsFirst,
            STATUS_KEYS['PICKUP_IGNORE_PATH']: instance.pickItemsIgnorePath,
            STATUS_KEYS['USE_WALLHACK']: instance.wallHack,
            STATUS_KEYS['AUTO_LOGIN']: instance.autoLogin,
        }

    def SaveStatus(self):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        file_handler_interface.dump_other_settings()

    def ReturnPickupFilter(self):
        return instance.pickFilter

    def SetPickupFilter(self, pickup_list):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        for item_id in instance.pickFilter:
            instance.delPickFilterItem(item_id)

        instance.pickFilter = []
        instance.addPickFilterItem(2)

        for item_id in pickup_list:
            if item_id == 2:
                continue
            instance.addPickFilterItem(item_id)

        file_handler_interface.dump_pickup_list()

    def GetPickupFilter(self):
        return instance.pickFilter

    def SwitchPickupItemFirst(self):
        if instance.pickItemsFirst:
            instance.OnChangePickItemFirst(False) 
        else:
            instance.OnChangePickItemFirst(True)         

    def SwitchPickupIgnorePath(self):
        if instance.pickItemsIgnorePath:
            instance.OnChangePickItemsIgnorePath(False)
        else:
            instance.OnChangePickItemsIgnorePath(True)

    def SwitchAutoLogin(self):
        if instance.autoLogin:
            instance.autoLogin = False
        else:
            instance.autoLogin = True

    def SwitchRestartHere(self):
        if instance.restartHere:
            instance.restartHere = False
        else:
            instance.restartHere = True
            if instance.restartInCity:
                self.SwitchRestartInCity()

    def SwitchRestartInCity(self):
        if instance.restartInCity:
            instance.restartInCity = False
        else:
            instance.restartInCity = True
            if instance.restartHere:
                self.SwitchRestartHere()

    def SwitchBluePotions(self):
        if instance.bluePotions:
            instance.bluePotions = False
        else:
            instance.bluePotions = True

    def SetMinMana(self, min_mana):
        instance.minMana = min_mana


    def SwitchRedPotions(self):
        if instance.redPotions:
            instance.redPotions = False
        else:
            instance.redPotions = True

    def SetMinHealth(self, min_health):
        instance.minHealth = min_health

    def SwitchSpeedHack(self):
        instance.OnSpeedHackOnOff()

    def SwitchAntiExp(self):
        if instance.antiExp:
            instance.antiExp = False
        else:
            instance.antiExp = True
    
    def SetSpeedMultiplier(self, speed_multiplier):
        instance.SetSpeedHackMultiplier(float(speed_multiplier))

    def SwitchPickup(self):
        if instance.pickUp:
            instance.pickUp = False
        else:
            instance.pickUp = True 

    def SetPickupRange(self, pickup_range):
        instance.SetPickupRange(pickup_range)

    
    def SetPickupSpeed(self, pickup_speed):
        instance.pickUpSpeed = pickup_speed

    def SwitchExcludeInFilter(self):
        if instance.excludeInFilter:
            instance.OnChangePickMode(False)
        else:
            instance.OnChangePickMode(True)     

    def SwitchUseRangePickup(self):
        if instance.useRangePickup:
            instance.useRangePickup = False
        else:
            instance.useRangePickup = True     
    
    def SwitchAvoidPlayersInPickup(self):
        if instance.doNotPickupIfPlayerHere:
            instance.doNotPickupIfPlayerHere = False
        else:
            instance.doNotPickupIfPlayerHere = True   

    def SwitchCheckIsWallBetweenPlayerAndItem(self):
        if instance.checkIsWallBetweenPlayerAndItem:
            instance.checkIsWallBetweenPlayerAndItem = False
        else:
            instance.checkIsWallBetweenPlayerAndItem = True  

    def SwitchWallhack(self):
        if instance.wallHack:
            instance.WallHackSwich(False)
        else:
            instance.WallHackSwich(True)

settings_interface = SettingsInterface()