#!/bin/bash

docker compose up -d kafka zookeeper redis 
sleep 5
docker compose up -d account-server
sleep 2
docker compose up -d game-server
sleep 7
docker compose up -d world-server