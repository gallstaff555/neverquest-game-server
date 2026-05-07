#!/bin/bash

docker stop sqlite && docker rm sqlite
docker ps -a
