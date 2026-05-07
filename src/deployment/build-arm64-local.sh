#!/bin/bash

sudo docker build -t neverquest-account-server:latest -f ../services/authentication/docker/local_arm64_Dockerfile .
sudo docker build -t neverquest-game-server:latest -f ../services/session/docker/local_arm64_Dockerfile .
sudo docker build -t neverquest-world-server:latest -f ../services/world_state/docker/Dockerfile .
