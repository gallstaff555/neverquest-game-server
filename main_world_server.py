#!/usr/bin/env python3

import redis, sys, time
from services.game.npc.npc_service import NPCService
from configuration.config import Config
from kafka import KafkaProducer
import logging
logging.basicConfig(
    format='[%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)


cfg = Config()

if __name__ == '__main__':

    try:
        logging.info("Creating redis connection...")
        redis = redis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, db=0, decode_responses=True)
        if redis.ping():
            logging.info(f"Redis is running on main_world_server service.")
    except:
        logging.info("Error connecting to redis.")
        sys.exit(1)

    try:
        logging.info(f"Creating Kafka Producer. Connection to {cfg.BOOTSTRAP_SERVER} on port {cfg.BOOTSTRAP_PORT}")
        producer = KafkaProducer(
            bootstrap_servers=f'{cfg.BOOTSTRAP_SERVER}:{cfg.BOOTSTRAP_PORT}'
            #value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # Serialize messages as JSON
            #key_serializer=lambda k: str(k).encode('utf-8')  # Optional: Serialize the key
        )
    except:
        logging.info("Error connecting to Kafka")
        sys.exit(1)

    time.sleep(1)

    npc_thread = NPCService(redis, producer)
    npc_thread.start()
    logging.info("Starting NPC thread.")