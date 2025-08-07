#!/usr/bin/env python3

import socketserver, json, time, threading, sys
sys.path.append('../../..')
from configuration.config import Config 
from kafka import KafkaConsumer
import logging
logging.basicConfig(
    format='[%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)

cfg = Config()

class ConnectionService(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, r):
        super().__init__(server_address, RequestHandlerClass)
        self.players = {} # Store the custom parameter
        self.players_marked_for_deletion = []
        self.npcs = {}
        self.r = r
        self.consumer = KafkaConsumer(cfg.NPC_UPDATES_TOPIC,
                        group_id=cfg.KAFKA_CONSUMER_GROUP_ID,
                        bootstrap_servers=[f'{cfg.BOOTSTRAP_SERVER}:{cfg.BOOTSTRAP_PORT}'],
                        auto_offset_reset='latest',  # Start from the latest offset
                        enable_auto_commit=False     # Don't commit offsets automatically
                        #consumer_timeout_ms=5000    # Stop if no message is received within 5 seconds
)

        self.update_redis_thread = threading.Thread(target=self.update_redis, daemon=True)
        self.update_redis_thread.start()
        logging.info("Redis update thread started.")

        self.update_npc_thread = threading.Thread(target=self.update_npcs, daemon=True)
        self.update_npc_thread.start()
        logging.info("npc update thread started.")

    def update_redis(self):
        update_timer = 1
        while True:
            if len(self.players_marked_for_deletion) > 0:
                self.check_for_disconnected_players()
            for player, value in self.players.items():
                self.r.set(player, json.dumps(value['pos']))
            time.sleep(update_timer)

    def update_npcs(self):
        update_timer = 1
        count = 0
        while True:
            for msg in self.consumer:
                count = count + 1
                record_dict = {
                    'topic': msg.topic,
                    'partition': msg.partition,
                    'offset': msg.offset,
                    'key': msg.key.decode('utf-8') if msg.key else None,
                    'value': msg.value.decode('utf-8') if msg.value else None
                }
                # TODO filter message by topic and partition when separating update by world zone
                npc_id = json.loads(record_dict.get('value')).get('npc_id')
                npc_value = record_dict.get('value')
                logging.info(f"npc_value: {npc_value}")
                self.npcs[npc_id] = npc_value

                logging.info(f"kafka msg count: {count}")

            time.sleep(update_timer)
            
    def check_for_disconnected_players(self):
        for player in self.players_marked_for_deletion:
            if player in self.players:
                del self.players[player]
                logging.info(f"{player} has been removed from the game.")
            else:
                logging.info(f"Player marked for deletion: {player} was not found!")
            # TODO don't delete player, but mark them as offline
            self.r.delete(player)
            logging.info(f"{player} has been removed from redis cache.")
        self.players_marked_for_deletion = []
        logging.info(f"Remaining player count: {len(self.players)}")
    


# override default handler class so we can use custom parameters
# use self.server.arg1 to access server data field
class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        raw_data = self.request.recv(2048).strip()
        if not raw_data:
            logging.info(f"Client {self.client_address} may have disconnected")
        else:
            decoded_data = raw_data.decode("utf-8").replace("'", "\"")
            payload = json.loads(decoded_data)
            header = payload['header']
            if header is None:
                logging.info("Error: no header provided.")
            elif header == "update":
                self.handle_update(payload)
            elif header == "disconnect":
                self.handle_disconnect(payload)
            elif header == "connect":
                self.handle_connection(payload)
            else:
                logging.info("Error with message occurred.")

            player_data = json.dumps(self.server.players)
            npc_data = json.dumps(self.server.npcs)

            players = {}
            players["players"] = player_data
            npcs = {}
            npcs["npcs"] = npc_data

            response = json.dumps([players, npcs])
            self.request.sendall(response.encode('utf-8'))

    def handle_connection(self, payload):
        player_name = f"{payload['name']}"
        if not player_name in self.server.players:
            logging.info(f"Player {player_name} connected for first time.")
        self.server.players[player_name] = payload
        logging.info(f"{player_name} connected!")

    def handle_disconnect(self, payload):
        player_name = f"{payload['name']}"
        logging.info(f"Player {player_name} wants to disconnect...")
        if player_name in self.server.players:
            self.server.players_marked_for_deletion.append(player_name)
        else:
            logging.info(f"Could not find {player_name} in list of players.")
        
    
    def handle_update(self, payload):
        player_name = f"{payload['name']}"
        self.server.players[player_name] = payload
        


