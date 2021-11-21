from OpenBot.Modules import OpenLib, Hooks
from OpenBot.Modules.OpenLog import DebugPrint
import serverInfo, background, ui, chat, net, app, introLogin # introLogin gives ServerStateChecker module
from OpenBot.Modules.Settings.settings_interface import settings_interface


def __PhaseChangeChannelCallback(phase,phaseWnd):
    global instance
    if instance.currState == STATE_NONE:
        return
    else:
        if phase == OpenLib.PHASE_GAME:
            instance.SetStateNone()
        elif phase == OpenLib.PHASE_SELECT:
            OpenLib.SetTimerFunction(instance.break_between_logins, phaseWnd.SelectStart)


def getCallBackWithArg(func, arg):
    return lambda: func(arg)

STATE_NONE = 0
STATE_CHANGING_CHANNEL = 1

class ChannelSwitcher(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.channels = {}
        self.currChannel = 0
        self.currState = STATE_NONE
        self.selectedChannel = 0
        self.current_channel = 0
        self.break_between_logins = 0.5
        self.last_time_break_between_logins = 0
        self.last_time = 0

    def GetRegionID(self):
        # FOR EU IS 0
        return 0

    def GetServerID(self):
        server_name = OpenLib.GetCurrentServer()
        region_id = self.GetRegionID()
        if server_name:
            for server in serverInfo.REGION_DICT[region_id].keys():
                if serverInfo.REGION_DICT[region_id][server]['name'] == server_name:
                    return int(server)

    def GetChannels(self):
        del self.channels
        self.channels = {}
        region_id = self.GetRegionID()
        server_id = self.GetServerID()

        try:
            channelDict = serverInfo.REGION_DICT[region_id][server_id]['channel']
        except:
            chat.AppendChat(3, '[ChannelSwitcher] Error while get channels')
            return

        for channelID, channelDataDict in channelDict.items():

            self.channels[int(channelID)] = {
                'id': int(channelID),
                'name': channelDataDict['name'],
                'ip': channelDataDict['ip'],
                'port': channelDataDict['tcp_port'],
                'acc_ip' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['ip'],
                'acc_port' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['port']
            }

    def IsSpecialMap(self):
        maps = {
            "season1/metin2_map_oxevent",
            "season2/metin2_map_guild_inside01",
            "season2/metin2_map_empirewar01",
            "season2/metin2_map_empirewar02",
            "season2/metin2_map_empirewar03",
            "metin2_map_dragon_timeattack_01",
            "metin2_map_dragon_timeattack_02",
            "metin2_map_dragon_timeattack_03",
            "metin2_map_skipia_dungeon_boss",
            "metin2_map_skipia_dungeon_boss2",
            "metin2_map_devilsCatacomb",
            "metin2_map_t1",
            "metin2_map_t2",
            "metin2_map_t3",
            "metin2_map_t4",
            "metin2_map_t5",
            "metin2_map_wedding_01",
            "metin2_map_duel"
        }
        if str(background.GetCurrentMapName()) in maps:
            return True
        return False

    def ConnectToChannel(self):
        if OpenLib.IsInGamePhase():
            net.Disconnect()
        net.ConnectTCP(self.selectedChannel["ip"], self.selectedChannel["port"])

    def ConnectToGame(self):
        net.SendEnterGamePacket()

    def ChangeChannelById(self, id):
        if int(id) not in self.channels:
            chat.AppendChat(3, "[Channel-Switcher] - Channel " + str(id) + " doesn't exist")
            return
        
        if self.IsSpecialMap():
            chat.AppendChat(3, "[Channel-Switcher] - You are on special map!")
            return           

        self.selectedChannel = self.channels[int(id)]
        self.currState = STATE_CHANGING_CHANNEL
        self.ConnectToChannel()

    def SetStateNone(self):
        self.selectedChannel = 0
        self.currState = STATE_NONE

    def OnUpdate(self):
        val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)
        if not val:
            return

        if OpenLib.IsInGamePhase():
            self.current_channel = OpenLib.GetCurrentChannel()

        if OpenLib.IsInLoginPhase():
            DebugPrint('LOGIN PHASE')
            if self.currState == STATE_CHANGING_CHANNEL:
                self.ConnectToChannel()

            if settings_interface.GetStatus()['AutoLogin'] and self.currState == STATE_NONE:
                self.ChangeChannelById(self.current_channel)

    def __del__(self):
        Hooks.deletePhaseCallback("channelCallback")

instance = ChannelSwitcher()
Hooks.registerPhaseCallback("channelCallback", __PhaseChangeChannelCallback)