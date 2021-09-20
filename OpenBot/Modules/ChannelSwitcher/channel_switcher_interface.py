from OpenBot.Modules.ChannelSwitcher.channel_switcher_module import instance
from OpenBot.Modules import OpenLib


class ChannelSwitcherInterface:

    def SetStatus(self, status):
        if 'ChangeChannel' in status.keys():
            self.ConnectToChannelByID(status['ChangeChannel'])

    def GetStatus(self):
        instance.GetChannels()
        return {
            'Channels': instance.channels
        }

    def ConnectToChannelByID(self, _id):
        instance.ChangeChannelById(_id)
    
    def GetNextChannel(self):
        current_channel = OpenLib.GetCurrentChannel()

        if not current_channel:
            return 0
        if current_channel + 1 > len(instance.channels):
            current_channel = 1
        else:
            current_channel += 1
        
        return current_channel

channel_switcher_interface = ChannelSwitcherInterface()