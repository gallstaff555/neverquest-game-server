#!/bin/bash

sudo docker build -t neverquest-account-server:latest -f docker/account-server/Dockerfile .
sudo docker build -t neverquest-game-server:latest -f docker/game-server/Dockerfile .