#!/usr/bin/env python3 

from .npc_behavior import NPCBehavior
import logging
logging.basicConfig(
    format='[%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO
)

class NPCFactory():
    def create_npc(self, npc_class, id, start_location):
        if npc_class == "healer":
            return Healer(id, start_location)
        else:
            raise ValueError("Invalid npc type cannot be created")

class NPC():
    def __init__(self, id, start_location):
        self.id = id
        self.location = start_location
        self.npc_class = None
        self.race = None
        self.flipped = False
        self.moving = False
        self.attacking = False
        self.is_updated = True
        self.behavior = NPCBehavior(self)
        logging.info(f"New NPC ID: {self.id} at start location: {self.location}")

class Healer(NPC):
    def __init__(self, id, start_location):
        super().__init__(id, start_location)
        self.npc_class = "healer"
        self.race = "human"
        logging.info("Creating a healer npc")
        logging.info(f"ID: {self.id}")
        logging.info(f"Start location: {self.location}")

    