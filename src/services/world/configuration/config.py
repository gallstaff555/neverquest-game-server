#!/usr/bin/env python3 

import logging

class Config:

    NPC_UPDATES_TOPIC = 'npc-updates'
    KAFKA_PARTITION_1 = 'partition1'
    KAFKA_CONSUMER_GROUP_ID = 'group1'

    TCP_HOST, TCP_PORT = "0.0.0.0", 5001


    FRESHINSTALL = True
    TEST = True
    DOCKER = False


    if DOCKER:
        REDIS_HOST, REDIS_PORT = 'redis', 6379
        BOOTSTRAP_SERVER, BOOTSTRAP_PORT = 'kafka', 9092 # TODO confirm if this should be 29092 for docker network
    else:
        REDIS_HOST, REDIS_PORT = 'localhost', 6379
        BOOTSTRAP_SERVER, BOOTSTRAP_PORT = 'localhost', 29092

    def setup_logging(self):
        logging.basicConfig(
        format='[%(filename)s:%(lineno)d] %(message)s',
        level=logging.INFO
    )