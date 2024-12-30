#!/usr/bin/env python3 

class NPCFactory():
    def create_npc(self, npc_class, id, start_location):
        if npc_class == "placeholder":
            return Placeholder(id, start_location)
        elif npc_class == "healer":
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
        print(f"ID: {self.id}")
        print(f"Start location: {self.location}")


class Placeholder(NPC):
    def __init__(self, id, start_location):
        super().__init__(id, start_location)
        self.npc_class = "placeholder"
        print("Creating a placeholder npc")
        print(f"ID: {self.id}")
        print(f"Start location: {self.location}")

class Healer(NPC):
    def __init__(self, id, start_location):
        super().__init__(id, start_location)
        self.npc_class = "healer"
        self.race = "human"
        print("Creating a healer npc")
        print(f"ID: {self.id}")
        print(f"Start location: {self.location}")

    