#!/usr/bin/env python3 

import threading, time, json, sys
sys.path.append('../../..')
from configuration.config import Config 
from .npc_factory import NPCFactory
from kafka import KafkaProducer
import logging
logging.basicConfig(
    format='[%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)


# create NPC
# update NPC position and status
# broadcast NPC location to client

# TODO only update npc info when there is a change or addition

cfg = Config()

class NPCService(threading.Thread):
    def __init__(self, redis, producer):
        super().__init__()
        self.factory = NPCFactory()
        self.producer = producer
        self.next_id = 1
        self.npc_list = []
        self.redis = redis

    def create_npc(self, npc_class, start_coords):
        new_npc = self.factory.create_npc(npc_class, self.next_id, start_coords) 
        self.npc_list.append(new_npc)
        self.next_id = self.next_id + 1

    # TODO update topic if there is a change to NPC to send to client 
    def publish_npc_update(self, npc_id, npc_class, location, race, flipped, moving, attacking):
        payload = {
            "npc_id": npc_id,
            "timestamp": int(time.time()),
            "npc_class": npc_class,
            "race": race,
            "pos": location,
            "flipped": flipped,
            "moving": moving,
            "attacking": attacking
        }

        try:
            logging.info(f"sending message to topic: {cfg.NPC_UPDATES_TOPIC}")
            self.producer.send(
                cfg.NPC_UPDATES_TOPIC,
                key=str(cfg.KAFKA_PARTITION_1).encode('utf-8'),  
                value=json.dumps(payload).encode('utf-8') 
            )
            self.producer.flush()
        except Exception as e:
            logging.info(f"Kafka producer error: {e}")
        

    def setup(self):
        self.create_npc("healer", f"{(150, 150)}")
        self.create_npc("healer", f"{(190, 190)}")

    def run(self):
        self.setup()
        while(True):
            
            # Publish NPC data to topic only if NPC is_updated flag is true 
            for npc in self.npc_list:
                if npc.is_updated:
                    try:
                        self.publish_npc_update(npc.id, npc.npc_class, npc.location, 
                                                npc.race, npc.flipped, npc.moving, npc.attacking)
                        npc.is_updated = False

                    except Exception as e:
                        logging.info(f"Exception raised while publishing npc update in npc_service run: {e}")

            # Iterate over players and NPCs and update NPCs in response to player movement or actions
            for npc in self.npc_list:
                for player in self.redis.scan_iter():
                    npc.behavior.respond_to_player(player, self.redis.get(player))


            time.sleep(1)
        