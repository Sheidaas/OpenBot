import websocket, websocket_server
import logging

all_clients = []
metin_clients = []
frontend_clients = []

def new_client(client, server):
    all_clients.append(client)
    server.send_message_to_all('A new clinet joined')

def message_received(client, server, message):
    
    if message == 'frontend_client':
        all_clients.remove(client)
        frontend_clients.append(client)
        server.send_message(client, 'You are a frontend client!')
        print(all_clients, frontend_clients, metin_clients)

server = websocket_server.WebsocketServer(13254, host="127.0.0.1", loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(message_received)
server.run_forever()