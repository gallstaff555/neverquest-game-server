#!/usr/bin/env python3

from services.game.npc.npc_service import NPCService


if __name__ == '__main__':
    
    npc_thread = NPCService()
    npc_thread.start()
    print("Starting NPC thread.")