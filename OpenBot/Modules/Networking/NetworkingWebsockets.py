from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
from OpenBot.Modules.Settings.settings_interface import settings_interface
from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface
from OpenBot import simplejson as json
import ui, chat
import eXLib
from OpenBot.Modules import UIComponents, OpenLog, OpenLib
import net_parser

server_url = 'ws://localhost:13254'

def OnMessage(id, message):
    global instance
    instance.isConnected = True

    if not instance.settedClientType:
        instance.SetClientTypeAsMetin()
        instance.settedClientType = True

    cleaned_message = json.loads(message)
    #OpenLog.DebugPrint(str(cleaned_message))
    if cleaned_message['type'] == 'actions':
        from OpenBot.Modules.Actions import ActionLoader
        raw_action_dict = {
            'actions': cleaned_message['data']['message']
        }
        OpenLog.DebugPrint(str(type(raw_action_dict['actions'])))
        cleaned_action_dict = ActionLoader.instance.ValidateRawActions(raw_action_dict)
        print('cleaned', cleaned_action_dict)
        if cleaned_action_dict:
            from OpenBot.Modules.Actions import ActionBot
            for action in cleaned_action_dict:
                ActionBot.instance.AddNewAction(action)

    elif cleaned_message['type'] == 'update':
       # OpenLog.DebugPrint(str(cleaned_message.keys()))
        if cleaned_message['data']['module'] == 'FarmBot':
            farmbot_interface.SetStatus(cleaned_message['data']['message'])
            #OpenLog.DebugPrint(str(farmbot_interface.GetStatus()))
        
        elif cleaned_message['data']['module'] == 'WaitHack':
            waithack_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'Settings':
            settings_interface.SetStatus(cleaned_message['data']['message'])
        
        elif cleaned_message['data']['module'] == 'SkillBot':
            skillbot_interface.SetStatus(cleaned_message['data']['message'])

class NetworkingWebsockets(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.lastTime = 0
        self.timeLastUpdate = 0
        self.timeToUpdate = 1
        self.isConnected = False
        self.settedClientType = False
        self.socket_to_server = eXLib.OpenWebsocket(server_url, OnMessage)
        #OpenLog.DebugPrint(str(self.socket_to_server))
        self.BuildWindow()

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

    def SetClientTypeAsMetin(self):
        data = {'type': 'set_role', 'data': {'message': 'metin2_client'}},
        respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateCharacterStatus(self):
        parsed_character_status = net_parser.parse_character_status_info()
        if parsed_character_status:
            data = {'type': 'information', 'data': {'message': parsed_character_status, 'action': 'set_character_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateInstancesListOnServer(self):
        parsed_instances_list = net_parser.parse_instances_list()
        if parsed_instances_list:
            data = {'type': 'information', 'data': {'message': parsed_instances_list, 'action': 'set_vids'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateHackStatus(self):
        parsed_hack_status = net_parser.parse_hack_status()
        #OpenLog.DebugPrint(str(parsed_hack_status))
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.01)
        if val and OpenLib.IsInGamePhase():
            if self.settedClientType and self.isConnected:
                val, self.timeLastUpdate = OpenLib.timeSleep(self.timeLastUpdate, self.timeToUpdate)
                if val:
                    self.UpdateInstancesListOnServer()
                    self.UpdateCharacterStatus()
                    self.UpdateHackStatus()



instance = NetworkingWebsockets()
instance.Show()
