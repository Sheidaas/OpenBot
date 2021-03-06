from OpenBot.Modules.Farmbot.farmbot_interface import farmbot_interface
from OpenBot.Modules.WaitHack.waithack_interface import waithack_interface
from OpenBot.Modules.Settings.settings_interface import settings_interface
from OpenBot.Modules.Skillbot.skillbot_interface import skillbot_interface
from OpenBot.Modules.InstanceInteractions.InstanceInteractionsInterface import instance_interactions_interface
from OpenBot import simplejson as json
from OpenBot.Modules import Movement
import ui, chat
import eXLib
from OpenBot.Modules import UIComponents, OpenLog, OpenLib
import net_parser
import encodings,imp, os # Import for Encoding Load
from OpenBot.Modules.OpenThreads import OpenThread


Thread = OpenThread()


STATES = {
    'WAITING': 'WAITING',
    'SENDING_PACKETS': 'SENDING_PACKETS',
}

server_url = 'ws://localhost:13254'

def OnMessage(id, message):
    global instance
    instance.isConnected = True

    if not instance.settedClientType:
        instance.SetClientTypeAsMetin()
        instance.settedClientType = True

    try:
        cleaned_message = json.loads(message)
    except:
        return
    #OpenLog.DebugPrint(str(cleaned_message))
    if cleaned_message['type'] == 'actions':
        if cleaned_message['data']['message'][0]['function'] == 'TeleportToPosition':
            x = cleaned_message['data']['message'][0]['function_args'][0][0]
            y = cleaned_message['data']['message'][0]['function_args'][0][1]
            map_name = cleaned_message['data']['message'][0]['function_args'][1]
            Movement.TeleportToPosition(x, y)
            return

        from OpenBot.Modules.Actions import ActionLoader
        raw_action_dict = {
            'actions': cleaned_message['data']['message']
        }
        cleaned_action_dict = ActionLoader.instance.ValidateRawActions(raw_action_dict)
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
            channel_switcher_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'FishBot':
            from OpenBot.Modules.Fishbot.fishbot_interface import fishbot_interface
            fishbot_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'FileHandler':
            from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
            file_handler_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'ShopSearcher':
            from OpenBot.Modules.ShopSearcher.shop_searcher_interface import shop_searcher_interface
            shop_searcher_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'Inventory':
            from OpenBot.Modules.Inventory.inventory_interface import inventory_interface
            inventory_interface.SetStatus(cleaned_message['data']['message'])
            instance.packetToSendQueue.append(instance.UpdateInventoryStatus)
        
        elif cleaned_message['data']['module'] == 'PickupFilter':
            settings_interface.SetPickupFilter(cleaned_message['data']['message']['pickup_filter'])
            instance.packetToSendQueue.append(instance.UpdatePickupFilter)

        elif cleaned_message['data']['module'] == 'InstanceInteractions':
            instance_interactions_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'Protector':
            from OpenBot.Modules.Protector.protector_interface import protector_interface
            protector_interface.SetStatus(cleaned_message['data']['message'])

        elif cleaned_message['data']['module'] == 'Attacker':
            from OpenBot.Modules.Attacker.attacker_interface import attacker_interface
            attacker_interface.SetStatus(cleaned_message['data']['message'])

    elif cleaned_message['type'] == 'update_request':
        if cleaned_message['data']['action'] == 'GET_INVENTORY_STATUS':
            instance.packetToSendQueue.append(instance.UpdateInventoryStatus)
        
        elif cleaned_message['data']['action'] == 'GET_PICKUP_FILTER':
            instance.packetToSendQueue.append(instance.UpdatePickupFilter)
        
        elif cleaned_message['data']['action'] == 'SET_NEW_SCHEMA':
            from OpenBot.Modules.Schema.SchemaLoader import schemaLoader
            from OpenBot.Modules.Schema.schema_runner_interface import schema_runner_interface
            schema = schemaLoader.LoadSchema(cleaned_message['data']['message'])
            if schema:
                OpenLog.DebugPrint(str(schema))
                schema_runner_interface.SetNewSchema(schema)


class NetworkingWebsockets(ui.ScriptWindow):

    def __init__(self):
        self.currentState = STATES['WAITING']
        ui.Window.__init__(self)
        self.lastTimeSendPacket = 0
        self.lastTime = 0
        self.timeLastUpdate = 0
        self.timeToUpdateBasicInformation = 0.3
        self.isConnected = False
        self.settedBasicInformation = False
        self.settedClientType = False
        self.socket_to_server = None
        self.created_thread = False
        self.encoding = OpenLib.GetCurrentMetinLanguage()


        ##
        # loading correct encoding into python
        encoding = imp.load_source(self.encoding, os.path.join(eXLib.PATH, 'OpenBot', 'lib', 'encodings', self.encoding+'.py'))
        encodings._cache[self.encoding] = encoding.getregentry()

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
        data = {'type': 'set_role', 'data': {'message': 'metin2_client', 'language': self.encoding }}
        eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateInventoryStatus(self):
        iventory_staus = net_parser.parse_inventory_status()
        #OpenLog.DebugPrint(str(iventory_staus))
        if iventory_staus:
            data = {'type': 'information', 'data': {'message': iventory_staus, 'action': 'set_inventory_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdatePickupFilter(self):
        pickup_filter = net_parser.parse_pickup_filter()
        if pickup_filter:
            data = {'type': 'information', 'data': {'message': pickup_filter, 'action': 'set_pickup_filter'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateBasicCharacterInformation(self):
        parsed_character_status = net_parser.parse_character_status_info()
        if parsed_character_status:
            data = {'type': 'information', 'data': {'message': parsed_character_status, 'action': 'set_character_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateCharacterStatus(self):
        parsed_character_status = net_parser.parse_character_status_info()
	    #OpenLog.DebugPrint(str(parsed_character_status))
        if parsed_character_status:
            data = {'type': 'information', 'data': {'message': parsed_character_status, 'action': 'set_character_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateInstancesListOnServer(self):
        parsed_instances_list = net_parser.parse_instances_list()
        if parsed_instances_list:
            data = {'type': 'information', 'data': {'message': parsed_instances_list, 'action': 'set_vids'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateSkillbotStatus(self):
        parsed_hack_status = net_parser.parse_skill_bot_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateActionbotStatus(self):
        try:
            parsed_hack_status = net_parser.parse_action_bot_status()
            if parsed_hack_status:
                data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
                data = net_parser.convertToUTF8(data,self.encoding)
                eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))
        except:
            OpenLog.DebugPrint('ERROR')
            OpenLog.DebugPrint(str(net_parser.parse_action_bot_status()))
    
    def UpdateWaithackStatus(self):
        parsed_hack_status = net_parser.parse_wait_hack_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateSettingsStatus(self):
        parsed_hack_status = net_parser.parse_settings_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data,self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateFarmbotStatus(self):
        parsed_hack_status = net_parser.parse_farm_bot_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateAttackerStatus(self):
        parsed_hack_status = net_parser.parse_attacker()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))
    
    def UpdateChannelSwitcherStatus(self):
        parsed_hack_status = net_parser.parse_channel_switcher_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateFishbotStatus(self):
        parsed_hack_status = net_parser.parse_fishbot_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateShopSearcherModule(self, shop):
        socket = self.socket_to_server
        def update_shops():
            parsed_hack_status = net_parser.parse_shop_searcher(shop)
            if parsed_hack_status:
                data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'append_shop_search'}}
                data = net_parser.convertToUTF8(data, self.encoding)
                eXLib.SendWebsocket(socket, json.dumps(data))
        return update_shops

    def UpdateInstanceInteractionsStatus(self):
        parsed_hack_status = net_parser.parse_instance_interaction_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateFileHandler(self):
        parsed_hack_status = net_parser.parse_file_handler()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateProtector(self):
        parsed_hack_status = net_parser.parse_protector_status()
        if parsed_hack_status:
            data = {'type': 'information', 'data': {'message': parsed_hack_status, 'action': 'set_hack_status'}}
            data = net_parser.convertToUTF8(data, self.encoding)
            eXLib.SendWebsocket(self.socket_to_server, json.dumps(data))

    def UpdateHackStatus(self):

        self.UpdateSkillbotStatus()
        self.UpdateActionbotStatus()
        self.UpdateWaithackStatus()
        self.UpdateSettingsStatus()
        self.UpdateFarmbotStatus()
        self.UpdateChannelSwitcherStatus()
        self.UpdateFishbotStatus()
        self.UpdateFileHandler()
        self.UpdateInstanceInteractionsStatus()
        self.UpdateProtector()
        self.UpdateAttackerStatus()

    def UpdateMethod(self):
        self.UpdateInstancesListOnServer()
        self.UpdateCharacterStatus()
        self.UpdateHackStatus()

    def OnUpdate(self):
        if self.currentState == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 3)
            if val:
                if self.socket_to_server is None:
                    self.socket_to_server = eXLib.OpenWebsocket(server_url, OnMessage)
                self.currentState = STATES['SENDING_PACKETS']

        elif self.currentState == STATES['SENDING_PACKETS'] and OpenLib.IsInGamePhase():
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, self.timeToUpdateBasicInformation)
            if val:
                if self.settedClientType and self.isConnected:
                    self.packetToSendQueue.append(self.UpdateInstancesListOnServer)
                    self.packetToSendQueue.append(self.UpdateCharacterStatus)
                    self.packetToSendQueue.append(self.UpdateHackStatus)
            #if not self.created_thread:
            #    self.created_thread = True
            #    Thread.createLoopedThread(self.UpdateMethod, [], False, False, False, False, 'networking')

            val, self.lastTimeSendPacket = OpenLib.timeSleep(self.lastTimeSendPacket, 0.05)
            if val:
                self.SendPacketFromQueue()

        else:
            self.currentState = STATES['WAITING']
            self.settedBasicInformation = False

'''


'''
instance = NetworkingWebsockets()
instance.Show()