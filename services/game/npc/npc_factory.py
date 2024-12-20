#!/usr/bin/env python3 

class NPCFactory():
    def create_npc(self, npc_type, id, start_location):
        if npc_type == "placeholder":
            return Placeholder(id, start_location)
        else:
            raise ValueError("Invalid npc type cannot be created")

class NPC():
    def __init__(self, id, start_location):
        self.id = id
        self.location = start_location
        print("Creating a placeholder npc")
        print(f"ID: {self.id}")
        print(f"Start location: {self.location}")
    
    def getId(self):
        return self.id
    
    def getLocation(self):
        return self.location

class Placeholder(NPC):
    def __init__(self, id, start_location):
        super().__init__(id, start_location)
        print("Creating a placeholder npc")
        print(f"ID: {self.id}")
        print(f"Start location: {self.location}")


    