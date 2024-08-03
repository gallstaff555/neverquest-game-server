#!/bin/bash

docker run --name sqlite -dit -v "./databases:/databases" -w /databases keinos/sqlite3