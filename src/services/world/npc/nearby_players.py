#!/usr/bin/env python3

import sys
from configuration.config import Config 
import logging

cfg = Config()
cfg.setup_logging()

class NearbyPlayers():
    def __init__(self):
        self.nearby_players = {} # key: name -- value: [distance, x, y]
        self.nearest_player = None
        self.nearest_player_dist = sys.maxsize
        self.nearest_player_x = None 
        self.nearest_player_y = None

    def add_player(self, player, distance, player_x, player_y):
        self.nearby_players[player] = [distance, player_x, player_y]
        if distance < self.nearest_player_dist:
            self.nearest_player_dist = distance 
            self.nearest_player = player
            self.nearest_player_x = player_x
            self.nearest_player_y = player_y

    def get_player_distance(self, player):
        return self.nearby_players.get(player)
    
    def get_player_found(self, player):
        return player in self.nearby_players
        
    def delete_player(self, player):
        player_was_nearest = (player == self.nearest_player)
        deleted = self.nearby_players.pop(player, None)
        if len(self.nearby_players) == 0:
            self.nearest_player = None 
            self.nearest_player_dist = sys.maxsize
            self.nearest_player_x = None 
            self.nearest_player_y = None

        elif deleted is not None and player_was_nearest:
            # Update nearest player dist and nearest player in event we just removed the nearest player
            self.nearest_player_dist = min(v[0] for v in self.nearby_players.values())
            self.nearest_player = next((k for k, v in self.nearby_players.items()
                                        if v[0] == self.nearest_player_dist), None)
            if self.nearest_player is not None:
                self.nearest_player_x = self.nearby_players[self.nearest_player][1]
                self.nearest_player_y = self.nearby_players[self.nearest_player][2]
            else:
                self.nearest_player_x = None
                self.nearest_player_y = None

        
    def get_nearby_player_list(self):
        return self.nearby_players
    
    def get_nearest_player(self):
        return self.nearest_player
    
    def get_nearest_player_dist(self):
        return self.nearest_player_dist