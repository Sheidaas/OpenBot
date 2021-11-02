from OpenBot.Modules.WaitHack.waithack_module import instance
from OpenBot.Modules.OpenLog import DebugPrint

class WaithackInterface():

    def SetStatus(self, status):
        good_keys = ['Enabled', 'Range', 'Speed','MaxMonsters','AvoidPlayers','AttackBlockedMonsters','UseCloudExploit', 'AttackPlayer', 'IsWallBetween']
        if not type(status) == dict:
            return False
        
        for key in status.keys():
            if key not in good_keys:
                return False

        if status['Enabled']:
            self.Start()
        else:
            self.Stop()
        
        DebugPrint(str(status))
        if instance.range != status['Range']:
            self.SetRange(status['Range'])
        if instance.speed != status['Speed']:
            self.SetSpeed(status['Speed'])
        if instance.maxMonster != status['MaxMonsters']:
            self.SetMaxMonsters(status['MaxMonsters'])
        if instance.avoidPlayers != status['AvoidPlayers']:
            self.SwitchAvoidPlayers()
        if instance.use_cloud_exploit != status['UseCloudExploit']:
            self.SwitchUseCloudExploit()
        if instance.attackPlayer != status['AttackPlayer']:
            self.SwitchAttackPlayer()
        if instance.is_wall_between != status['IsWallBetween']:
            self.SwitchIsWallBetween()
        if instance.attack_blocked_monsters != status['AttackBlockedMonsters']:
            self.SwitchAttackBlockedMonsters()

        self.SaveStatus()

    def SaveStatus(self):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        file_handler_interface.dump_other_settings()

    def GetStatus(self):
        return {
            'Enabled': instance.enabled,
            'Range': instance.range,
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
        instance.onEnableChange(True)
    
    def Stop(self):
        instance.enabled = False
        instance.onEnableChange(False)
    
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
