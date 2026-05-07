#!/usr/bin/env python3

import threading, redis, time, sys
from connection_service import ConnectionService, TCPHandler
from configuration.config import Config
import logging


cfg = Config()
cfg.setup_logging()

class PersistentLocationThread(threading.Thread):
    def __init__(self, r):
        super().__init__()


    def run(self):
        while True:
            try:
                time.sleep(2)
                for player in r.scan_iter():
                    coords = r.get(player)
                    logging.info(f"{player} pos: {coords}")
                
            except Exception as e:
                logging.info(f"Exception raised: {e}")
                

if __name__ == "__main__":


    try:
        r = redis.Redis(host=cfg.REDIS_HOST, port=cfg.REDIS_PORT, db=0, decode_responses=True)
        if r.ping():
            logging.info(f"Redis is running on main_game_server service.")
        if cfg.FRESHINSTALL:
            logging.info(f"Freshinstall is enabled. Wiping all existing data from redis.")
            r.flushall()
    except:
        logging.info("Error connecting to redis.")
        #os.sys("exit") #sys.exit?

    try: 
        persistent_location_thread = PersistentLocationThread(r)
        persistent_location_thread.start()
        logging.info("Persistent location thread created.")
        

        player_thread = threading.Thread(target=ConnectionService((cfg.TCP_HOST, cfg.TCP_PORT), TCPHandler, r).serve_forever)
        player_thread.start()
        logging.info(f"Persistent player position thread created. Updating redis on port {cfg.REDIS_PORT}.")
        logging.info(f"Game server started on port {cfg.TCP_PORT}.")
    except Exception as e:
        logging.info(f"Error occured while initializing game server threads: {e}")

    