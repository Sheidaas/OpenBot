from OpenBot.Modules.ChannelSwitcher.channel_switcher_module import instance
from OpenBot.Modules.Actions import Action, ActionRequirementsCheckers, ActionFunctions
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
from OpenBot.Modules import OpenLib

STATE_NONE = 0
STATE_CHANGING_CHANNEL = 1

class ChannelSwitcherInterface:

    def SetStatus(self, status):
        if 'ChangeChannel' in status.keys():
            action_dict = {
                'function_args': [status['ChangeChannel']],
                'function': ActionFunctions.ChangeChannel,
                'requirements': {
                    ActionRequirementsCheckers.IS_IN_CHANNEL: [status['ChangeChannel']]},
                'on_success': [Action.NEXT_ACTION],
            }
            action_bot_interface.AddAction(action_dict)

    def GetStatus(self):
        return {
            'Channels': self.GetChannels()
        }

    def GetCurrentState(self):
        return instance.currState

    def GetChannels(self):
        instance.GetChannels()
        return instance.channels

    def ConnectToChannelByID(self, _id):
        instance.ChangeChannelById(_id)
    
    def GetNextChannel(self):
        current_channel = OpenLib.GetCurrentChannel()
        if not current_channel:
            return 0
        if current_channel + 1 > len(self.GetChannels()):
            current_channel = 1
        else:
            current_channel += 1
        
        return current_channel

channel_switcher_interface = ChannelSwitcherInterface()