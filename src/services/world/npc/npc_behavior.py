#!/usr/bin/env python3 

import math
from .nearby_players import NearbyPlayers 
from configuration.config import Config 
import logging

cfg = Config()
cfg.setup_logging()

class NPCBehavior():
    def __init__(self, npc):
        self.npc = npc
        self.aggro_range = 100
        self.sq_aggro_range = 2000
        self.nearby_players = NearbyPlayers()

    # Determine player proximity; TODO use for aggro radius later
    def handle_player_nearby(self, my_location, player, player_data):
        player_x, player_y = player_data
        npc_x, npc_y = my_location
        sq_distance_from_player = self.get_squared_distance_to_player(player_x, player_y, npc_x, npc_y)
        if (sq_distance_from_player < self.sq_aggro_range):
            self.nearby_players.add_player(player, sq_distance_from_player, player_x, player_y)
        # Player should be removed from nearby_player list because they are outside of aggro radius
        elif (self.nearby_players.get_player_found(player)):
            self.nearby_players.delete_player(player)
        
        # Handle nearest player in range
        nearest_player = self.nearby_players.nearest_player
        if (nearest_player is not None and nearest_player == player):
            #logging.info(f"Nearest player to NPC: {self.npc.id} is {self.nearby_players.get_nearest_player()} at distance of {self.nearby_players.get_nearest_player_dist()}")
            self.npc_orientation(player_x, npc_x)

    # Better performance if we only need to find the closest player
    def get_squared_distance_to_player(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return dx * dx + dy * dy

    # Accurate distance rounded to nearest int 
    def get_distance_to_player(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return int(round(distance))
    
    # determine whether to flip or not flip npc
    def npc_orientation(self, player_x, npc_x):
        if (player_x < npc_x and not self.npc.flipped):
            self.npc.flipped = True 
            self.npc.is_updated = True 
        elif (player_x >= npc_x and self.npc.flipped):
            self.npc.flipped = False
            self.npc.is_updated = True 

    def run(self, player, player_data):
        self.handle_player_nearby(self.npc.location, player, player_data)
