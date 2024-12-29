#!/usr/bin/env python3 

class Config:
    NPC_UPDATES_TOPIC = 'npc-updates'
    KAFKA_PARTITION_1 = 'partition1'
    KAFKA_CONSUMER_GROUP_ID = 'group1'

    TCP_HOST, TCP_PORT = "0.0.0.0", 5001

    TEST = True

    if TEST:
        REDIS_HOST, REDIS_PORT = 'localhost', 6379
    else:
        REDIS_HOST, REDIS_PORT = 'redis', 6379