from OpenBot.Modules.Actions import ActionBotInterface
from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
from OpenBot.Modules.Settings.settings_interface import settings_interface
from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface
from OpenBot import simplejson as json
import ui, chat
import eXLib
from OpenBot.Modules import UIComponents, OpenLog, OpenLib
import net_parser
import codecs

server_url = 'ws://localhost:13254'

def OnMessage(id, message):
    global instance
    instance.isConnected = True

    if not instance.settedClientType:
        instance.SetClientTypeAsMetin()
        instance.settedClientType = True
    
    if not instance.settedBasicInformation:
        instance.settedBasicInformation = True
        pass

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
            from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
            for action in cleaned_action_dict:
                action_bot_interface.AddAction(action)

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

        elif cleaned_message['data']['module'] == 'ActionBot':
            from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
            action_bot_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'ChannelSwitcher':
            from OpenBot.Modules.ChannelSwitcher.channel_switcher_interface import channel_switcher_interface
            OpenLog.DebugPrint(str(cleaned_message['data']['message']))
            channel_switcher_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'Inventory':
            from OpenBot.Modules.Inventory.inventory_interface import inventory_interface
            #OpenLog.DebugPrint(str(cleaned_message['data']['message']))
            inventory_interface.SetStatus(cleaned_message['data']['message'])
            instance.packetToSendQueue.append(instance.UpdateInventoryStatus)
        
        elif cleaned_message['data']['module'] == 'PickupFilter':
            #OpenLog.DebugPrint(str(cleaned_message['data']['message']['pickup_filter']))
            settings_interface.SetPickupFilter(cleaned_message['data']['message']['pickup_filter'])
            instance.packetToSendQueue.append(instance.UpdatePickupFilter)

    elif cleaned_message['type'] == 'update_request':
        if cleaned_message['data']['action'] == 'GET_INVENTORY_STATUS':
            instance.packetToSendQueue.append(instance.UpdateInventoryStatus)
        
        elif cleaned_message['data']['action'] == 'GET_PICKUP_FILTER':
            instance.packetToSendQueue.append(instance.UpdatePickupFilter)
        
        elif cleaned_message['data']['action'] == 'SET_NEW_SCHEMA':
            from OpenBot.Modules.Schema.SchemaLoader import schemaLoader
            from OpenBot.Modules.Schema.schema_runner_interface import schema_runner_interface
            schema_runner_interface.SetNewSchema(schemaLoader.LoadSchema(cleaned_message['data']['message']))


class NetworkingWebsockets(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.lastTimeSendPacket = 0
        self.lastTime = 0
        self.timeLastUpdate = 0
        self.timeToUpdateBasicInformation = 1
        self.isConnected = False
        self.settedBasicInformation = False
        self.settedClientType = False
        self.socket_to_server = eXLib.OpenWebsocket(server_url, OnMessage)



        self.packetToSendQueue = []
        #OpenLog.DebugPrint(str(self.socket_to_server))
        self.BuildWindow()

    def __del__(self):
        ui.Window.__del__(self)

    def BuildWindow(self):
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(150, 100)
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

    def SendPacketFromQueue(self):
        #OpenLog.DebugPrint(str(self.packetToSendQueue))
        if self.packetToSendQueue:
            packet_to_send = self.packetToSendQueue.pop()
            packet_to_send()

    def SetClientTypeAsMetin(self):
        #read encoding: 
        try:
            file = open(eXLib.PATH+'loca.cfg') 
            enc = file.readlines()[0].split[' '][0]
        except:
            file = open(eXLib.PATH+'loca.cfg') 
            enc = file.readlines()[0].split[' '][1]
        
        if(len(enc)!= 4):
            print('Cannot Read Encoding from File!')
        data = {'type': 'set_role', 'data': {'message': 'metin2_client', 'data': enc}}
        respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateInventoryStatus(self):
        iventory_staus = net_parser.parse_inventory_status()
        #OpenLog.DebugPrint(str(iventory_staus))
        if iventory_staus:
            data = {'type': 'information', 'data': {'message': iventory_staus, 'action': 'set_inventory_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))         

    def UpdatePickupFilter(self):
        pickup_filter = net_parser.parse_pickup_filter()
        if pickup_filter:
            data = {'type': 'information', 'data': {'message': pickup_filter, 'action': 'set_pickup_filter'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))  

    def UpdateBasicCharacterInformation(self):
        parsed_character_status = net_parser.parse_character_status_info()
        if parsed_character_status:
            data = {'type': 'information', 'data': {'message': parsed_character_status, 'action': 'set_character_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))        

    def UpdateCharacterStatus(self):
        parsed_character_status = net_parser.parse_character_status_info()
	    #OpenLog.DebugPrint(str(parsed_character_status))
        if parsed_character_status:
            data = {'type': 'information', 'data': {'message': parsed_character_status, 'action': 'set_character_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateInstancesListOnServer(self):
        parsed_instances_list = net_parser.parse_instances_list()
        if parsed_instances_list:
            data = {'type': 'information', 'data': {'message': parsed_instances_list, 'action': 'set_vids'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateSkillbotStatus(self):
        parsed_hack_status = net_parser.parse_skill_bot_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateActionbotStatus(self):
        try:
            parsed_hack_status = net_parser.parse_action_bot_status()
            if parsed_hack_status:
                data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
                respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))
        except:
            OpenLog.DebugPrint('ERROR')
            OpenLog.DebugPrint(str(net_parser.parse_action_bot_status()))
    
    def UpdateWaithackStatus(self):
        parsed_hack_status = net_parser.parse_wait_hack_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateSettingsStatus(self):
        parsed_hack_status = net_parser.parse_settings_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateFarmbotStatus(self):
        parsed_hack_status = net_parser.parse_farm_bot_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))
    
    def UpdateChannelSwitcherStatus(self):
        parsed_hack_status = net_parser.parse_channel_switcher_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            respond = eXLib.SendWebsocket(self.socket_to_server, json.dumps(data, ensure_ascii=False))

    def UpdateHackStatus(self):
        self.packetToSendQueue.append(self.UpdateSkillbotStatus)
        self.packetToSendQueue.append(self.UpdateActionbotStatus)
        self.packetToSendQueue.append(self.UpdateWaithackStatus)
        self.packetToSendQueue.append(self.UpdateSettingsStatus)
        self.packetToSendQueue.append(self.UpdateFarmbotStatus)
        self.packetToSendQueue.append(self.UpdateChannelSwitcherStatus)

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, self.timeToUpdateBasicInformation)
        if val:
            if self.settedClientType and self.isConnected:
                self.packetToSendQueue.append(self.UpdateInstancesListOnServer)
                self.packetToSendQueue.append(self.UpdateCharacterStatus)
                self.packetToSendQueue.append(self.UpdateHackStatus)

        val, self.lastTimeSendPacket = OpenLib.timeSleep(self.lastTimeSendPacket, 0.05)
        if val:
            self.SendPacketFromQueue()

        if not OpenLib.IsInGamePhase():
            self.settedBasicInformation = False



instance = NetworkingWebsockets()
instance.Show()