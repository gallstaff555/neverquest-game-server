# python virtual env
python3 -m venv .venv
source .venv/bin/activate

# install redis testing
brew install redis
brew service start redis 
redis-cli ping

# set up database
# this also happens automatically when you run main_account_server.py
cd persistence/
sqlite3 neverquest.db < scripts/create_tables.sql

# TODO
Add configuration file with hosts, ports, and timer values 
Work on world service to store game map and fixed objects
Work on game_service to add enemies to world 

Fix return characters who have no user_id foreign key. Make sure these can't be created or returned without a valid fk
