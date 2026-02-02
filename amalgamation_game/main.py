"""
AMALGAMATION GAME - Prize-Winning Tournament Framework

Main entry point for the Amalgamation Game. Launch from command line:
    python main.py
    
Or import as module:
    from amalgamation_game.main import launch_game
"""

import sys
from ui.game_ui import main

if __name__ == "__main__":
    print("=" * 70)
    print("AMALGAMATION - Prize-Winning Game Framework".center(70))
    print("=" * 70)
    print("\n🏆 Launching Amalgamation Game Tournament Platform...\n")
    
    main()
