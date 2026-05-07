# python virtual env
python3 -m venv .venv
source .venv/bin/activate

# required docker containers
docker compose up -d kafka zookeeper redis

# install redis testing manually
brew install redis
brew service start redis 
redis-cli ping

# set up database
(this also happens automatically when you run main_account_server.py)
cd persistence/
sqlite3 neverquest.db < scripts/create_tables.sql

# service start order
docker compose up -d kafka redis zookeeper
./main_game_server.py
./main_world_server.py

# TODO
Only send updated data when a change is detected, e.g. when a player or NPC moves 
Store player location persistently
Make NPC separate class from Otherplayer in client
Make child hostile class from NPC class 

Fix return characters who have no user_id foreign key. Make sure these can't be created or returned without a valid fk
