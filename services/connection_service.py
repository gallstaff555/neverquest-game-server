#!/usr/bin/env python3

import socketserver, json, time, redis, threading

class ConnectionService(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, r):
        super().__init__(server_address, RequestHandlerClass)
        self.players = {} # Store the custom parameter
        self.players_marked_for_deletion = []
        self.r = r

        self.update_redis_thread = threading.Thread(target=self.update_redis, daemon=True)
        self.update_redis_thread.start()


    def update_redis(self):
        update_timer = 1
        while True:
            if len(self.players_marked_for_deletion) > 0:
                self.check_for_disconnected_players()
            for player, value in self.players.items():
                self.r.set(player, json.dumps(value['pos']))
            time.sleep(update_timer)
            
    def check_for_disconnected_players(self):
        for player in self.players_marked_for_deletion:
            if player in self.players:
                del self.players[player]
                print(f"{player} has been removed from the game.")
            else:
                print(f"Player marked for deletion: {player} was not found!")
            self.r.delete(player)
            print(f"{player} has been removed from redis cache.")
        self.players_marked_for_deletion = []
        print(f"Remaining player count: {len(self.players)}")

# override default handler class so we can use custom parameters
# use self.server.arg1 to access server data field
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw_data = self.request.recv(2048).strip()
        if not raw_data:
            print(f"Client {self.client_address} may have disconnected")
        else:
            decoded_data = raw_data.decode("utf-8").replace("'", "\"")
            payload = json.loads(decoded_data)
            header = payload['header']
            if header is None:
                print("Error: no header provided.")
            elif header == "update":
                self.handle_update(payload)
            elif header == "disconnect":
                self.handle_disconnect(payload)
            elif header == "connect":
                self.handle_connection(payload)
            else:
                print("Error with message occurred.")
            result_string = json.dumps(self.server.players)
            self.request.sendall(result_string.encode('utf-8'))

    def handle_connection(self, payload):
        player_name = f"{payload['name']}"
        if not player_name in self.server.players:
            print(f"Player {player_name} connected for first time.")
        self.server.players[player_name] = payload
        #self.server.r.set(player_name, json.dumps(payload['pos']))
        print(f"{player_name} connected!")

    def handle_disconnect(self, payload):
        player_name = f"{payload['name']}"
        print(f"Player {player_name} wants to disconnect...")
        if player_name in self.server.players:
            self.server.players_marked_for_deletion.append(player_name)
        else:
            print(f"Could not find {player_name} in list of players.")
        

    def handle_update(self, payload):
        player_name = f"{payload['name']}"
        self.server.players[player_name] = payload
        


