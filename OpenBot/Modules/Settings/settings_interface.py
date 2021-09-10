from OpenBot.Modules.Settings.settings_module import instance


class SettingsInterface:

    def SetStatus(self, status):
        if status['PickupRange'] != instance.pickUpRange:
            self.SetPickupRange(status['PickupRange'])

        if status['RestartHere'] != instance.restartHere:
            self.SwitchRestartHere()
        if status['RestartInCity'] != instance.restartInCity:
            self.SwitchRestartInCity()
        if status['BluePotions'] != instance.bluePotions:
            self.SwitchBluePotions()
        if status['MinMana'] != instance.minMana:
            self.SetMinMana(status['MinMana'])
        if status['RedPotions'] != instance.redPotions:
            self.SwitchRedPotions()       
        if status['MinHealth'] != instance.minHealth:
            self.SetMinHealth(status['MinHealth'])
        if status['SpeedHack'] != instance.speedHack:
            self.SwitchSpeedHack()    
        if status['AntiExp'] != instance.antiExp:
            self.SwitchAntiExp()
        if status['SpeedMultiplier'] != instance.speedMultiplier:
            self.SetSpeedMultiplier(status['SpeedMultiplier'])
        if status['Pickup'] != instance.pickUp:
            self.SwitchPickup()
        if status['PickupSpeed'] != instance.pickUpSpeed:
            self.SetPickupSpeed(status['PickupSpeed'])
        if status['ExcludeInFilter'] != instance.excludeInFilter:
            self.SwitchExcludeInFilter()
        if status['UseRangePickup'] != instance.useRangePickup:
            self.SwitchUseRangePickup()
        if status['AvoidPlayersInPickup'] != instance.doNotPickupIfPlayerHere:
            self.SwitchAvoidPlayersInPickup()
        #if status['CheckIsWallBetweenPlayerAndItem'] != instance.checkIsWallBetweenPlayerAndItem:
        #    self.SwitchCheckIsWallBetweenPlayerAndItem()
        if status['UseWallhack'] != instance.wallHack:
            self.SwitchWallhack()
        if status['AutoLogin'] != instance.autoLogin:
            self.SwitchAutoLogin()
        if status['PickupItemFirst'] != instance.pickItemsFirst:
            self.SwitchPickupItemFirst()

        _filter = instance.pickFilter
        instance.pickFilter = []
        for _id in _filter:
            instance.delPickFilterItem(_id)
        
        for _id in status['PickupFiltersID']:
            instance.addPickFilterItem(_id)

        instance.SaveSettings()

    def GetStatus(self):
        return {
            'RestartHere': instance.restartHere,
            'RestartInCity': instance.restartInCity,
            'BluePotions': instance.bluePotions,
            'MinMana': instance.minMana,
            'RedPotions': instance.redPotions,
            'MinHealth': instance.minHealth,
            'SpeedHack': instance.speedHack,
            'AntiExp': instance.antiExp,
            'SpeedMultiplier': instance.speedMultiplier,
            'Pickup': instance.pickUp,
            'PickupRange': instance.pickUpRange,
            'PickupSpeed': instance.pickUpSpeed,
            'ExcludeInFilter': instance.excludeInFilter,
            'UseRangePickup': instance.useRangePickup,
            'AvoidPlayersInPickup': instance.doNotPickupIfPlayerHere,
            'PickupItemFirst': instance.pickItemsFirst,
            'PickupIgnorePath': instance.pickItemsIgnorePath,
            #'CheckIsWallBetweenPlayerAndItem': instance.checkIsWallBetweenPlayerAndItem,
            'UseWallhack': instance.wallHack,
            'AutoLogin': instance.autoLogin,   
            'PickupFiltersID': instance.pickFilter
        }
    
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

    def SwitchRestartInCity(self):
        if instance.restartInCity:
            instance.restartInCity = False
        else:
            instance.restartInCity = True

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