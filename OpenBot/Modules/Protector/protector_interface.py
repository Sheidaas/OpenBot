from OpenBot.Modules.Protector.protector_module import protector_module

STATUS_KEYS = {
    'ENABLED': 'Enabled',
    'AVOID_PLAYERS': 'AvoidPlayers',
    'WHITELIST': 'Whitelist',
    'EXIT_METIN': 'ExitMetin',
    'LOGOUT': 'Logout',
    'CHANGE_CHANNEL': 'ChangeChannel',
    'SWITCH_OFF_WAITHACK': 'SwitchOffWaithack',
    'SWITCH_OFF_PICKUP': 'SwitchOffPickup',
    'TIME_TO_WAIT_IN_LOGIN_PHASE': 'TimeToWaitInLoginPhase'
}


class ProtectorInterface:


    def GetStatus(self):
        return {
            STATUS_KEYS['ENABLED']: protector_module.enabled,
            STATUS_KEYS['AVOID_PLAYERS']: protector_module.avoid_players,
            STATUS_KEYS['WHITELIST']: protector_module.whitelist,
            STATUS_KEYS['EXIT_METIN']: protector_module.exit_metin,
            STATUS_KEYS['LOGOUT']: protector_module.logout,
            STATUS_KEYS['CHANGE_CHANNEL']: protector_module.change_channel,
            STATUS_KEYS['SWITCH_OFF_WAITHACK']: protector_module.switch_off_waithack,
            STATUS_KEYS['SWITCH_OFF_PICKUP']: protector_module.switch_off_pickup,
            STATUS_KEYS['TIME_TO_WAIT_IN_LOGIN_PHASE']: protector_module.time_to_wait_in_login_phase
        }

    def SetStatus(self, status):
        for status_key in status.keys():

            if STATUS_KEYS['ENABLED'] == status_key:
                self.switch_enabled()
            elif STATUS_KEYS['AVOID_PLAYERS'] == status_key:
                self.switch_avoid_players()
            elif STATUS_KEYS['WHITELIST'] == status_key:
                self.set_whitelist(status[status_key])
            elif STATUS_KEYS['EXIT_METIN'] == status_key:
                self.switch_exit_metin()
            elif STATUS_KEYS['LOGOUT'] == status_key:
                self.switch_logout()
            elif STATUS_KEYS['CHANGE_CHANNEL'] == status_key:
                self.switch_change_channel()
            elif STATUS_KEYS['SWITCH_OFF_WAITHACK'] == status_key:
                self.switch_waithack()
            elif STATUS_KEYS['SWITCH_OFF_PICKUP'] == status_key:
                self.switch_pickup()
            elif STATUS_KEYS['TIME_TO_WAIT_IN_LOGIN_PHASE'] == status_key:
                self.set_time_to_wait_in_login_phase(status[status_key])

    @staticmethod
    def switch_enabled():
        protector_module.enabled = not protector_module.enabled

    @staticmethod
    def switch_avoid_players():
        protector_module.avoid_players = not protector_module.avoid_players

    @staticmethod
    def set_whitelist(new_whitelist):
        protector_module.whitelist = new_whitelist

    @staticmethod
    def switch_exit_metin():
        protector_module.exit_metin = not protector_module.exit_metin

    @staticmethod
    def switch_logout():
        protector_module.logout = not protector_module.logout

    @staticmethod
    def switch_change_channel():
        protector_module.change_channel = not protector_module.change_channel

    @staticmethod
    def switch_waithack():
        protector_module.switch_off_waithack = not protector_module.switch_off_waithack

    @staticmethod
    def switch_pickup():
        protector_module.switch_off_pickup = not protector_module.switch_off_pickup

    @staticmethod
    def set_time_to_wait_in_login_phase(new_time):
        protector_module.time_to_wait_in_login_phase = new_time

protector_interface = ProtectorInterface()
