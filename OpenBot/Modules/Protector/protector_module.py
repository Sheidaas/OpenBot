from OpenBot.Modules.radar_module import radar_module
from OpenBot.Modules.ChannelSwitcher.channel_switcher_interface import channel_switcher_interface
from OpenBot.Modules import OpenLib
from OpenBot.Modules.Settings.settings_interface import settings_interface
from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
from OpenBot.Modules.Actions import ActionFunctions, ActionRequirementsCheckers, Action
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
from OpenBot.Modules import Hooks
import ui
import chr
import app
import chat

STATES = {
    'WAITING': 'WAITING',
    'RUNNING': 'RUNNING'
}

def _afterLoadPhase(phase, phaseWnd):
    global protector_module
    if OpenLib.IsInGamePhase():
        protector_module.current_state = STATES['WAITING']


class ProtectorModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.enabled = True
        self.current_state = STATES['WAITING']
        self.avoid_players = True
        self.whitelist = []  # players names
        self.exit_metin = False
        self.logout = False
        self.change_channel = False
        self.switch_off_waithack = False
        self.is_waithack_switched = False
        self.switch_off_pickup = False
        self.is_pickup_switched = False
        self.is_unknown_player_close = False

        self.is_current_action_done = True
        self.time_to_wait_in_login_phase = 5
        self.last_time = 0

    def on_current_action_done_callback(self):
        self.is_current_action_done = True

    def OnUpdate(self):
        if not self.enabled:
            return

        if self.current_state == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 6)
            if val:
                self.current_state = STATES['RUNNING']

        elif self.current_state == STATES['RUNNING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)
            #chat.AppendChat(3, 'something')
            if not val:
                return

            if not self.avoid_players:
                return

            players_off_the_whitelist = [player_name for player_name in radar_module.players
                                         if player_name not in self.whitelist]

            if not players_off_the_whitelist:
                self.is_unknown_player_close = False


            for player_vid in players_off_the_whitelist:

                if chr.GetNameByVID(player_vid) in self.whitelist:
                    continue

                self.is_unknown_player_close = True
                return





"""
                if self.is_waithack_switched:
                    waithack_interface.Start()
                    self.is_waithack_switched = False

                if self.is_pickup_switched:
                    settings_interface.SwitchPickup()
                    self.is_pickup_switched = False
                    
                if self.change_channel and self.is_current_action_done:
                    self.is_current_action_done = False
                    self.current_state = STATES['WAITING']
                    action_dict = {
                        'function_args': [channel_switcher_interface.GetNextChannel()],
                        'function': ActionFunctions.ChangeChannel,
                        'callback': self.on_current_action_done_callback,
                        'requirements': {
                            ActionRequirementsCheckers.IS_IN_CHANNEL: [channel_switcher_interface.GetNextChannel()]},
                        'on_success': [Action.NEXT_ACTION],
                    }
                    action_bot_interface.AddAction(action_dict)

                if self.exit_metin:
                    app.Abort()

                if self.switch_off_waithack:
                    if not self.is_waithack_switched:
                        waithack_interface.Stop()
                        self.is_waithack_switched = True

                if self.switch_off_pickup:
                    if not self.is_pickup_switched:
                        settings_interface.SwitchPickup()
                        self.is_pickup_switched = True
"""




protector_module = ProtectorModule()
protector_module.Show()
Hooks.registerPhaseCallback('protector_module', _afterLoadPhase)

