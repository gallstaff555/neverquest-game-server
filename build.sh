#!/bin/bash

#docker build . -t neverquest-game-server:latest
sudo docker build -t neverquest-game-server:latest -f docker/game-server/Dockerfile .