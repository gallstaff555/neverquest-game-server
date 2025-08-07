#!/usr/bin/env python3 

import math, ast
import logging
logging.basicConfig(
    format='[%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)

class NPCBehavior():
    def __init__(self, npc):
        self.npc = npc
        self.aggro_range = 100

    # Determine player proximity; TODO use for aggro radius later
    def check_if_player_nearby(self, my_location, player, player_data):
        player_x, player_y = ast.literal_eval(player_data)
        self_x, self_y = ast.literal_eval(my_location)
        distance_from_player = self.get_distance_to_player(player_x, player_y, self_x, self_y)
        
        # TODO this was just a test; there is bug where if first NPC is far away, NPCs won't be flipped
        if (distance_from_player < self.aggro_range):
            logging.info(f"Player {player} distance is {distance_from_player} from NPC {self.npc.id}")
            self.npc.flipped = True 
            self.npc.is_updated = True 
        else:
            self.npc.flipped = False
            self.npc.is_updated = True 


    def get_distance_to_player(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance
    
    def respond_to_player(self, player, player_data):
        self.check_if_player_nearby(self.npc.location, player, player_data)