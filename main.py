#!/usr/bin/env python3

import threading, redis, os, time
from player_service.player_connection import PlayerConnection, TCPHandler

class PersistentLocationThread(threading.Thread):
    def __init__(self, r):
        super().__init__()


    def run(self):
        while True:
            try:
                time.sleep(2)
                all_keys = r.keys('*')
                for key in all_keys:
                    print(f"{key} pos: {r.get(key)}")
                
            except Exception as e:
                print(f"Exception raised: {e}")
                

if __name__ == "__main__":

    REDIS_HOST, REDIS_PORT = 'localhost', 6379
    TCP_HOST, TCP_PORT = "0.0.0.0", 5001

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        if r.ping():
            print(f"Redis is running.")
    except:
        print("Error connecting to redis.")
        os.sys("exit")

    try: 
        persistent_location_thread = PersistentLocationThread(r)
        persistent_location_thread.start()
        print("Persistent location thread created.")
        player_thread = threading.Thread(target=PlayerConnection((TCP_HOST, TCP_PORT), TCPHandler, r).serve_forever)
        player_thread.start()
        print(f"Persistent player position thread created. Updating redis on port {REDIS_PORT}.")
        print(f"Game server started on port {TCP_PORT}.")
    except Exception as e:
        print(f"Error occured while initializing game server threads: {e}")

    