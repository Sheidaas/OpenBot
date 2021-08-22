from Resources.Modules import simplejson as json
import ui, chat
import eXLib
import UIComponents
import net_parser

server_url = 'ws://localhost:13254'

def printConnectedToServer():
    chat.AppendChat(3, 'Connected to local server')


class NetworkingWebsockets(ui.Window):

    def __init__(self):
        ui.Window.__init__(self)
        self.socket_to_server = eXLib.OpenWebsocket(server_url, printConnectedToServer)
        self.BuildWindow()

        self.SetClientTypeAsMetin()

    def SetClientTypeAsMetin(self):
        data = {'type': 'set_role', 'data': {'message': 'metin2_client'}},
        eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateInstancesListOnServer(self):
        parsed_instances_list = net_parser.parse_instances_list()
        data = {'type': 'information', 'data': {'message': parsed_instances_list, 'action': 'append_vids'}}
        eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(300, 500)
        self.Board.SetCenterPosition()
        self.Board.AddFlag('movable')
        self.Board.AddFlag('float')
        self.Board.SetTitleName('Networking Window')
        self.Board.SetCloseEvent(self.Close)
        self.Board.Hide()

        self.comp = UIComponents.Component()

        self.refreshVids = self.comp.Button(self.pickupTab, 'Refresh vids', '', 20, 30, self.UpdateInstancesListOnServer,
                                              'd:/ymir work/ui/public/Middle_Button_01.sub',
                                              'd:/ymir work/ui/public/Middle_Button_02.sub',
                                              'd:/ymir work/ui/public/Middle_Button_03.sub')

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()



instance = NetworkingWebsockets()
