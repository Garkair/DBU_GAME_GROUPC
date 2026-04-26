#!/usr/bin/env python3
"""
Operation DBU: Reloaded
-----------------------
Entry point – run this file to start the game.
"""

import sys
import os

# Ensure the folder containing this file is on the path,
# so `game/` is always found even if you launch from another directory.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.game_engine import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
