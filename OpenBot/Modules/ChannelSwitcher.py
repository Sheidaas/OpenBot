from BotBase import BotBase
import OpenLib, UIComponents
import serverInfo, background, ui, chat, net, app, introLogin # introLogin gives ServerStateChecker module


class ChannelSwitcher(BotBase):

    def __init__(self):
        BotBase.__init__(self)
        self.channels = []

        self.BuildWindow()

    def BuildWindow(self):
        component = UIComponents.Component()

        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(200, 300)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('Channel Switcher')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        self.barItems, self.fileListBox, self.ScrollBar = component.ListBoxEx2(self.Board, 10, 10, 180, 100)

        self.connectButton = component.Button(self.Board, 'Connect', '', 10, 220, self.OnConnectButton,
                                          'd:/ymir work/ui/public/small_Button_01.sub',
                                          'd:/ymir work/ui/public/small_Button_02.sub',
                                          'd:/ymir work/ui/public/small_Button_03.sub')

        self.refreshButton = component.Button(self.Board, 'Refresh', '', 10, 250, self.OnRefreshButton,
                                          'd:/ymir work/ui/public/small_Button_01.sub',
                                          'd:/ymir work/ui/public/small_Button_02.sub',
                                          'd:/ymir work/ui/public/small_Button_03.sub')

    def OnRefreshButton(self):
        self.GetChannels()
        self.fileListBox.RemoveAllItems()
        for channel in self.channels:
            self.fileListBox.AppendItem(OpenLib.Item('Channel ' + str(channel['id'])))

    def _find_channel_by_name(self, name):
        str_id = name.split('Channel ')[1]
        chat.AppendChat(3, str(str_id))
        for channel in self.channels:
            if channel['id'] == int(str_id):
                return channel
        return False

    def OnConnectButton(self):
        _channel = self.fileListBox.GetSelectedItem()
        channel = self._find_channel_by_name(_channel.text)
        if not channel:
            chat.AppendChat(3, '[ChannelSwitcher] You did not select a channel')
            return

        region_id = self.GetRegionID()
        server_id = self.GetServerID()


        try:
            serverName = serverInfo.REGION_DICT[region_id][server_id]["name"]
            chat.AppendChat(3, str(serverName))
            chat.AppendChat(3, str(channel))
            channelName = serverInfo.REGION_DICT[region_id][server_id]["channel"][channel['id']]["name"]
            addrKey = serverInfo.REGION_DICT[region_id][server_id]["channel"][channel['id']]["key"]
            chat.AppendChat(3, str(addrKey))
            ip = serverInfo.REGION_DICT[region_id][server_id]["channel"][channel['id']]["ip"]
            chat.AppendChat(3, str(ip))
            tcp_port = serverInfo.REGION_DICT[region_id][server_id]["channel"][channel['id']]["tcp_port"]
            chat.AppendChat(3, str(tcp_port))
            state = serverInfo.REGION_DICT[region_id][server_id]["channel"][channel['id']]["state"]
            chat.AppendChat(3, str(state))
            account_ip = serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]["ip"]
            chat.AppendChat(3, str(account_ip))
            account_port = serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]["port"]
            chat.AppendChat(3, str(account_port))

            markKey = region_id * 1000 + server_id * 10
            markAddrValue = serverInfo.MARKADDR_DICT[markKey]
            net.SetMarkServer(markAddrValue["ip"], markAddrValue["tcp_port"])
            app.SetGuildMarkPath(markAddrValue["mark"])
            app.SetGuildSymbolPath(markAddrValue["symbol_path"])

        except:
            chat.AppendChat(3, '[ChannelSwitcher] An error occured while connect')
            return

       # if state == serverInfo.STATE_NONE:
       #     chat.AppendChat(1, "Sorry the selected channel is offline!")
       #     return
       # elif state == serverInfo.STATE_DICT[3]:
       #     chat.AppendChat(1, "Sorry the selected channel is full!")
       #     return
       # elif net.GetServerInfo().strip().split(", ")[1] == \
       #         self.ChannelList.textDict[self.ChannelList.selectedLine].strip().split(" ")[0]:
       #     chat.AppendChat(1, "You are already on the selected channel!")
       #     return
        if self.IsSpecialMap():
           chat.AppendChat(1, "Sorry in this area you cannot change channel without logout!")
           return

        self.DirectConnect(ip, tcp_port, account_ip, account_port)


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
        self.channels = []
        region_id = self.GetRegionID()
        server_id = self.GetServerID()

        try:
            channelDict = serverInfo.REGION_DICT[region_id][server_id]['channel']
        except:
            chat.AppendChat(3, '[ChannelSwitcher] Error while get channels')
            return

        for channelID, channelDataDict in channelDict.items():
            self.channels.append({
                'id': channelID,
                'name': channelDataDict['name'],
                'state': channelDataDict['state']
            })

    def IsSpecialMap(self):
        maps = [
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
            "metin2_map_deviltower1",
            "metin2_map_t1",
            "metin2_map_t2",
            "metin2_map_t3",
            "metin2_map_t4",
            "metin2_map_t5",
            "metin2_map_wedding_01",
            "metin2_map_duel"
        ]
        if str(background.GetCurrentMapName()) in maps:
            return True
        return False

    def DirectConnect(self, ip, tcp_port, accout_ip, account_port):
        net.ConnectToAccountServer(ip, tcp_port, accout_ip, account_port)

        net.SendSelectCharacterPacket(0)
        net.SendEnterGamePacket()

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.OnRefreshButton()
            self.Board.Show()