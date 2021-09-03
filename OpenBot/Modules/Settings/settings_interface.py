from OpenBot.Modules.Settings.settings_module import instance


class SettingsInterface:

    def SetStatus(self, status):
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
        if status['CheckIsWallBetweenPlayerAndItem'] != instance.checkIsWallBetweenPlayerAndItem:
            self.SwitchCheckIsWallBetweenPlayerAndItem()
        if status['UseWallhack'] != instance.wallHack:
            self.SwitchUseWallhack()

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
            'PickupSpeed': instance.pickUpSpeed,
            'ExcludeInFilter': instance.excludeInFilter,
            'UseRangePickup': instance.useRangePickup,
            'AvoidPlayersInPickup': instance.doNotPickupIfPlayerHere,
            'CheckIsWallBetweenPlayerAndItem': instance.checkIsWallBetweenPlayerAndItem,
            'UseWallhack': instance.wallHack,   
        }
    
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
        if not type(min_mana) == int:
            return False
        if min_mana >=0 and min_mana <= 100:
            instance.minMana = min_mana
        else:
            return False

    def SwitchRedPotions(self):
        if instance.redPotions:
            instance.redPotions = False
        else:
            instance.redPotions = True

    def SetMinHealth(self, min_health):
        if not type(min_health) == int:
            return False
        if min_health >= 0 and min_health <= 100:
            instance.minHealth = min_health
        else:
            return False

    def SwitchSpeedHack(self):
        if instance.speedHack:
            instance.speedHack = False
        else:
            instance.speedHack = True

    def SwitchAntiExp(self):
        if instance.antiExp:
            instance.antiExp = False
        else:
            instance.antiExp = True
    
    def SetSpeedMultiplier(self, speed_multiplier):
        if not type(speed_multiplier) == int or not type(speed_multiplier) == float:
            return False
        if speed_multiplier >= 1 and speed_multiplier <= 10:
            instance.speedMultiplier = float(speed_multiplier)
        else:
            return False

     def SwitchPickup(self):
        if instance.pickUp:
            instance.pickUp = False
        else:
            instance.pickUp = True 

    def SetPickupRange(self, pickup_range):
        if not type(pickup_range) == int or not type(pickup_range) == float:
            return False
        if pickup_range >= 100 and pickup_range <= 10000:
            instance.pickUpRange = float(pickup_range)
        else:
            return False
    
    def SetPickupSpeed(self, pickup_speed):
        if not type(pickup_speed) == int or not type(pickup_speed) == float:
            return False
        if pickup_speed >= 1 and pickup_range <= 10:
            instance.pickUpSpeed = float(pickup_speed)
        else:
            return False
    
    def SwitchExcludeInFilter(self):
        if instance.excludeInFilter:
            instance.excludeInFilter = False
        else:
            instance.excludeInFilter = True     

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