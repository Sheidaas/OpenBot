from OpenBot import simplejson as json
import ui, chat
import eXLib
from OpenBot.Modules import UIComponents, OpenLog, OpenLib
import net_parser

server_url = 'ws://localhost:13254'
connected = False

def SetConnected(id, message):
    global instance
    instance.isConnected = True
    OpenLog.DebugPrint(message)

class NetworkingWebsockets(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.lastTime = 0
        self.timeLastUpdate = 0
        self.timeToUpdate = 3
        self.isConnected = False
        self.settedClientType = False
        self.socket_to_server = eXLib.OpenWebsocket(server_url, SetConnected)
        #OpenLog.DebugPrint(str(self.socket_to_server))
        self.BuildWindow()


    def SetClientTypeAsMetin(self):
        data = {'type': 'set_role', 'data': {'message': 'metin2_client'}},
        respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))
        chat.AppendChat(3, str(respond))

        
    def UpdateInstancesListOnServer(self):
        parsed_instances_list = net_parser.parse_instances_list()
        if parsed_instances_list:
            data = {'type': 'information', 'data': {'message': parsed_instances_list, 'action': 'set_vids'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))
            chat.AppendChat(3, str(respond))

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(300, 500)
        self.Board.SetCenterPosition()
        self.Board.AddFlag('movable')
        self.Board.AddFlag('float')
        self.Board.SetTitleName('Networking Window')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        self.comp = UIComponents.Component()

        self.refreshVids = self.comp.Button(self.Board, 'Refresh vids', '', 20, 30, self.UpdateInstancesListOnServer,
                                              'd:/ymir work/ui/public/Middle_Button_01.sub',
                                              'd:/ymir work/ui/public/Middle_Button_02.sub',
                                              'd:/ymir work/ui/public/Middle_Button_03.sub')

        self.setAsMetin = self.comp.Button(self.Board, 'Set as metin', '', 20, 50, self.SetClientTypeAsMetin,
                                              'd:/ymir work/ui/public/Middle_Button_01.sub',
                                              'd:/ymir work/ui/public/Middle_Button_02.sub',
                                              'd:/ymir work/ui/public/Middle_Button_03.sub')
    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

    def UpdateInstancesList(self):
        self.UpdateInstancesListOnServer()

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime,0.1)
        if val and OpenLib.IsInGamePhase():
            if not self.settedClientType:
                self.SetClientTypeAsMetin()
                self.settedClientType = True

            if self.settedClientType and self.isConnected:
                val, self.timeLastUpdate = OpenLib.timeSleep(self.timeLastUpdate, self.timeToUpdate)
                if val:
                    self.UpdateInstancesList()



instance = NetworkingWebsockets()
instance.Show()
