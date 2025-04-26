#!/bin/bash

sudo docker build -t neverquest-account-server:latest -f docker/account-server/local_arm64_Dockerfile .
sudo docker build -t neverquest-game-server:latest -f docker/game-server/local_arm64_Dockerfile .
sudo docker build -t neverquest-world-server:latest -f docker/world-server/Dockerfile .
