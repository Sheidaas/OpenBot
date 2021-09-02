from OpenBot.Modules.WaitHack.waithack_module import instance


class WaithackInterface():

    def GetStatus(self):
        return {
            'Enabled': instance.enabled,
            'Range': instance.range * 100,
            'Speed': instance.speed,
            'MaxMonsters': instance.maxMonster,
            'AvoidPlayers': instance.avoidPlayers,
            'UseCloudExploit': instance.use_cloud_exploit,
            'AttackPlayer': instance.attackPlayer,
            'IsWallBetween': instance.is_wall_between,
            'AttackBlockedMonsters': instance.attack_blocked_monsters
        }
    
    def Start(self):
        instance.enabled = True
    
    def Stop(self):
        instance.enabled = False

    def LoadSettings(self):
        instance.loadSettings()
    
    def SaveSettings(self):
        instance.saveSettings()
    
    def SetRange(self, range_value):
        instance.range = range_value
        
    def SetSpeed(self, speed_value):
        instance.speed = speed_value
    
    def SetMaxMonsters(self, max_monsters_value):
        instance.maxMonster = max_monsters_value
    
    def SwitchAttackPlayer(self, val=None):
        if instance.attackPlayer:
            instance.attackPlayer = False
        else:
            instance.attackPlayer = True

    def SwitchAvoidPlayers(self, val=None):
        if instance.avoidPlayers:
            instance.avoidPlayers = False
        else:
            instance.avoidPlayers = True    

    def SwitchUseCloudExploit(self, val=None):
        if instance.use_cloud_exploit:
            instance.use_cloud_exploit = False
        else:
            instance.use_cloud_exploit = True

    def SwitchIsWallBetween(self, val=None):
        if instance.is_wall_between:
            instance.is_wall_between = False
        else:
            instance.is_wall_between = True

    def SwitchAttackBlockedMonsters(self, val=None):
        if instance.attack_blocked_monsters:
            instance.attack_blocked_monsters = False
        else:
            instance.attack_blocked_monsters = True

waithack_interface = WaithackInterface()
