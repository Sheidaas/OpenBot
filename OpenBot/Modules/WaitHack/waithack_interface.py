from OpenBot.Modules.WaitHack.waithack_module import instance


STATUS_KEYS = {
    'ENABLED': 'Enabled',
    'RANGE': 'Range',
    'SPEED': 'Speed',
    'MAX_MONSTERS': 'MaxMonsters',
    'ATTACK_BLOCKED_MONSTERS': 'AttackBlockedMonsters',
    'USE_CLOUD_EXPLOIT': 'UseCloudExploit',
    'IS_WALL_BETWEEN': 'IsWallBetween',
    'INSTANCE_TYPE_TO_ATTACK': 'InstanceTypeToAttack',
    'ATTACK_BOSSES': 'AttackBosses',
}


class WaithackInterface:

    def SetStatus(self, status, save_status=True):
        for status_key in status:

            if STATUS_KEYS['ENABLED'] == status_key:
                self.SwitchEnabled()
            elif STATUS_KEYS['RANGE'] == status_key:
                self.SetRange(status[status_key])

            elif STATUS_KEYS['SPEED'] == status_key:
                self.SetSpeed(status[status_key])

            elif STATUS_KEYS['MAX_MONSTERS'] == status_key:
                self.SetMaxMonsters(status[status_key])

            elif STATUS_KEYS['ATTACK_BLOCKED_MONSTERS'] == status_key:
                self.SwitchAttackBlockedMonsters()

            elif STATUS_KEYS['USE_CLOUD_EXPLOIT'] == status_key:
                self.SwitchUseCloudExploit()

            elif STATUS_KEYS['IS_WALL_BETWEEN'] == status_key:
                self.SwitchIsWallBetween()

            elif STATUS_KEYS['ATTACK_BOSSES'] == status_key:
                instance.attack_bosses = not instance.attack_bosses

            elif STATUS_KEYS['INSTANCE_TYPE_TO_ATTACK'] == status_key:
                instance.instance_type_to_attack = status[status_key
                ]
        if save_status: self.SaveStatus()

    def SaveStatus(self):
        from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
        file_handler_interface.dump_other_settings()

    def GetStatus(self):
        return {
            STATUS_KEYS['ENABLED']: instance.enabled,
            STATUS_KEYS['RANGE']: instance.range,
            STATUS_KEYS['SPEED']: instance.speed,
            STATUS_KEYS['MAX_MONSTERS']: instance.maxMonster,
            STATUS_KEYS['USE_CLOUD_EXPLOIT']: instance.use_cloud_exploit,
            STATUS_KEYS['IS_WALL_BETWEEN']: instance.is_wall_between,
            STATUS_KEYS['ATTACK_BLOCKED_MONSTERS']: instance.attack_blocked_monsters,
            STATUS_KEYS['INSTANCE_TYPE_TO_ATTACK']: instance.instance_type_to_attack,
            STATUS_KEYS['ATTACK_BOSSES']: instance.attack_bosses
        }

    def SwitchEnabled(self):
        if instance.enabled:
            self.Stop()
        else:
            self.Start()

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
