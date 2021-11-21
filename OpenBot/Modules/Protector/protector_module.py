from OpenBot.Modules.radar_module import radar_module
from OpenBot.Modules.ChannelSwitcher.channel_switcher_interface import channel_switcher_interface
from OpenBot.Modules import OpenLib
import ui
import chr
import app

STATES = {
    'WAITING': 'WAITING',
    'RUNNING': 'RUNNING'
}


class ProtectorModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__()
        self.enabled = False
        self.current_state = STATES['WAITING']
        self.avoid_players = False
        self.whitelist = []  # players names
        self.exit_metin = False
        self.logout = False
        self.change_channel = False
        self.switch_off_waithack = False
        self.switch_off_pickup = False

        self.is_current_action_done = True
        self.time_to_wait_in_login_phase = 0
        self.last_time = 0

    def OnUpdate(self):
        if not self.enabled:
            return

        if self.current_state == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 3)
            if val:
                self.current_state = STATES['RUNNING']

        elif self.current_state == STATES['RUNNING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)

            if not val:
                return

            if not self.avoid_players:
                return

            for player_vid in radar_module.players:

                if chr.GetNameByVID(player_vid) in self.whitelist:
                    continue

                if self.change_channel and self.is_current_action_done:
                    channel_switcher_interface.SetStatus({'ChangeChannel': channel_switcher_interface.GetNextChannel()})

                elif self.exit_metin:
                    app.Abort()

                if self.switch_off_waithack:
                    pass

                if self.switch_off_pickup:
                    pass


protector_module = ProtectorModule()
protector_module.Show()

