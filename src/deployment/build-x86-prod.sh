#!/bin/bash

sudo docker build -t neverquest-account-server:latest -f ../services/authentication/docker/Dockerfile .
sudo docker build -t neverquest-game-server:latest -f ../services/session/docker/Dockerfile .
sudo docker build -t neverquest-world-server:latest -f ../services/world_stater/docker/Dockerfile .
