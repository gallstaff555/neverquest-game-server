#!/usr/bin/env python3

import threading, redis, os, time
from player_service.player_connection import PlayerConnection, TCPHandler

class DataProcessorThread(threading.Thread):
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
    TCP_HOST, TCP_PORT = "0.0.0.0", 5000

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        if r.ping():
            print(f"Redis is running.")
    except:
        print("Error connecting to redis.")
        os.sys("exit")

    try: 
        data_processor_thread = DataProcessorThread(r)
        data_processor_thread.start()
        print("Data process thread created.")
        player_thread = threading.Thread(target=PlayerConnection((TCP_HOST, TCP_PORT), TCPHandler, r).serve_forever)
        player_thread.start()
        print("Player position thread created.")
        print("Game server started.")
    except Exception as e:
        print(f"Error occured while initializing game server threads: {e}")

    