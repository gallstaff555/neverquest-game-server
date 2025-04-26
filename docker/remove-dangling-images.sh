#!/bin/bash

sudo docker rmi $(docker images -f "dangling=true" -q)
