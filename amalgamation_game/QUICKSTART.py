"""
QUICK START GUIDE - Amalgamation Game

This guide walks through launching and playing the prize-winning tournament game.
"""

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                   🏆 AMALGAMATION QUICK START GUIDE 🏆                      ║
║                                                                              ║
║                    Prize-Winning Tournament Framework                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. INSTALLATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Requirements:
  • Python 3.8 or higher
  • tkinter (usually included with Python)
  • pip (Python package manager)

Installation steps:
  1. Navigate to the amalgamation_game directory
  2. (Optional) Create virtual environment:
     python -m venv venv
     venv\\Scripts\\activate  # Windows
     source venv/bin/activate  # Mac/Linux
  
  3. Install dependencies (if needed):
     pip install -r requirements.txt

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. LAUNCHING THE GAME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the main application:
  python main.py

This launches the Amalgamation Game UI with tournament management system.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. INTERFACE OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The UI consists of 5 main tabs:

[1] TOURNAMENT TAB
    • View tournament status
    • See prize breakdown ($10,000 total)
    • Manage tournament bracket
    • Start/Reset tournament progression
    
    Available Opponents:
    ⚜️  Royal Necromancer - Master-level strategic AI (163-IQ)
    ⚔️  Royal Guardian Commander - Squad-based tactical AI
    ♟️  3D Chess Master - Neural network chess engine

[2] SELECT OPPONENT TAB
    • Choose which AI opponent to face
    • Select difficulty level (Novice → Amalgamated)
    • Pick game mode (3D Chess, Guardian Combat, Trial, Neural Duel)
    • Click "START MATCH" to begin competition
    
    Difficulty Scaling:
    Level 1: Novice (50% strength)
    Level 2: Adept (100% strength - baseline)
    Level 3: Master (150% strength)
    Level 4: Legendary (200% strength)
    Level 5: Amalgamated (300% strength - extreme challenge)

[3] GAMEPLAY TAB
    • Real-time match display
    • Current score and round information
    • Time elapsed tracking
    • Move execution interface
    • Game end controls
    
    During Match:
    • "Execute Move" - Make your move/action against AI
    • "End Game" - Finish match and record result

[4] STATISTICS TAB
    • Your player profile and current level
    • Win/Loss/Draw record
    • Win percentage calculation
    • Elo rating (competitive skill rating)
    • Experience points and XP needed for next level
    • Achievement tracking with unlocked badges

[5] LEADERBOARD TAB
    • Tournament standings
    • Ranked players by Elo rating
    • Total wins/losses per competitor
    • Real-time ranking updates

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. GAMEPLAY SEQUENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step-by-step tournament match:

  1. TOURNAMENT SETUP
     → Tournament Tab → "Start Tournament"
     → Prize pool initialized ($10,000)
     → Bracket created with all opponents

  2. OPPONENT SELECTION
     → Select Opponent Tab
     → Choose opponent (Necromancer/Guardian/Chess AI)
     → Choose difficulty (Novice-Amalgamated)
     → Choose game mode (Chess/Combat/Trial/Neural/Royal)
     → Click "START MATCH"

  3. MATCH GAMEPLAY
     → Gameplay Tab displays active match
     → Your score vs Opponent score
     → Round counter and time tracking
     → Click "Execute Move" multiple times
     → Each move advances the game state
     → Scores update based on move outcomes

  4. GAME CONCLUSION
     → Click "End Game" to finish
     → System determines winner (Win/Loss/Draw)
     → Results recorded in your statistics
     → Elo rating updated based on opponent strength
     → Experience awarded (100 for win, 50 for draw, 25 for loss)
     → Check level-up (unlocks at 500 XP per level)

  5. PROGRESS TRACKING
     → Statistics Tab shows updated record
     → Leaderboard Tab shows new ranking
     → Return to Select Opponent Tab for next match

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. OPPONENT CHARACTERISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROYAL NECROMANCER (Master AI - 163-IQ Cognition)
├─ Starting Difficulty: Master level
├─ Cognition Type: High-IQ strategic pattern recognition
├─ Guardian Protocols:
│  ├─ CrownJeweller - Resource optimization
│  ├─ XNOR Blood Code - Logical consistency
│  └─ HighMind Circuit - Strategic synthesis
├─ Strategies: Aggressive/Defensive/Strategic/Balanced
├─ Special: Alignment tracking (good/evil scale)
└─ Challenge: Highly predictive AI with complex reasoning

ROYAL GUARDIAN COMMANDER (Tactical AI)
├─ Starting Difficulty: Adept level
├─ Combat Type: Squad-based tactical formations
├─ Squad Composition:
│  ├─ Sentinel - Fast/agile
│  ├─ Protector - Balanced
│  ├─ Warden - Defensive
│  └─ Paladin - High damage
├─ Formations: Diamond/Phalanx/Spear/Shield
├─ System: Morale-based squad coordination
└─ Challenge: Requires tactical counterplay

3D CHESS MASTER (Strategic AI)
├─ Starting Difficulty: Master level
├─ Board: 8×8×3 (three levels of chess)
├─ Evaluation: Minimax with neural network scoring
├─ Features:
│  ├─ Material counting
│  ├─ Positional evaluation
│  ├─ Capture tracking
│  └─ Endgame analysis
├─ AI Depth: Configurable search (2-6 moves ahead)
└─ Challenge: Superior positional understanding

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. PROGRESSION SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXPERIENCE & LEVELS:
  Level 1 → Level 2: 500 XP
  Level 2 → Level 3: 1000 XP
  Level 3 → Level 4: 1500 XP
  (500 XP per level increment)

MATCH REWARDS:
  Victory:  +100 XP, +1 Win, Elo adjustment
  Draw:     +50 XP,  +1 Draw, minimal Elo change
  Defeat:   +25 XP,  +1 Loss, -Elo adjustment

ELO RATING SYSTEM:
  Starting Rating: 1600 Elo
  K-Factor: 32 (standard in competitive play)
  Formula: New = Old + 32 × (Result - Expected)
  Expected = 1 / (1 + 10^((opponent_elo - your_elo) / 400))

ACHIEVEMENTS:
  • Level Milestones (Reached Level X)
  • Difficulty Conquests (Defeated Amalgamated)
  • Win Streaks (3+ consecutive victories)
  • Opponent Mastery (5+ wins vs same opponent)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. TIPS FOR SUCCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

vs ROYAL NECROMANCER:
  ✓ Vary your moves - don't follow predictable patterns
  ✓ Exploit alignment system - adjust your play style
  ✓ Watch for protocol activation - adapt strategy
  ✓ Consider morale - momentum shifts the game

vs ROYAL GUARDIAN COMMANDER:
  ✓ Break up formations - target weak points
  ✓ Focus on morale reduction - weaken squad cohesion
  ✓ Exploit individual guards - separate and conquer
  ✓ Build pressure - force poor formation choices

vs 3D CHESS MASTER:
  ✓ Control center positions - positional advantage
  ✓ Sacrifice material tactically - create weaknesses
  ✓ Look 5+ moves ahead - plan long-term strategy
  ✓ Master 3D movement - use vertical dimension

GENERAL STRATEGY:
  ✓ Start with Novice/Adept to learn mechanics
  ✓ Build Elo rating gradually against easier opponents
  ✓ Challenge Master/Legendary for big rewards
  ✓ Track win rates against each opponent
  ✓ Experiment with different game modes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "tkinter not found"
Solution: pip install tk  (or python3-tk on Linux)

Issue: "ModuleNotFoundError"
Solution: Ensure you're running from amalgamation_game directory
         python main.py (not python ../amalgamation_game/main.py)

Issue: Game won't start match
Solution: Select opponent, difficulty, AND game mode before clicking START MATCH

Issue: Buttons not responding
Solution: Close dialog boxes first, then try again

Issue: Stats not updating
Solution: Click "End Game" to save results before checking stats

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. SYSTEM REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MINIMUM:
  • Python 3.8+
  • 50 MB disk space
  • 512 MB RAM
  • tkinter library

RECOMMENDED:
  • Python 3.10+
  • 200 MB disk space
  • 2 GB RAM
  • Modern display (1920×1080+)

TESTED PLATFORMS:
  ✓ Windows 10/11
  ✓ macOS 10.15+
  ✓ Linux (Ubuntu 20.04+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. ADVANCED USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTING AS MODULE:
  from amalgamation_game.game_systems import GameEngine, Difficulty
  from amalgamation_game.opponents import NecromancerOpponent
  
  engine = GameEngine(player_name="YourName")
  opponent = NecromancerOpponent()
  engine.register_opponent(opponent)
  
  game = engine.start_game(
      mode=GameMode.CHESS_3D,
      difficulty=Difficulty.MASTER,
      opponent_id="necromancer_signet"
  )

CUSTOMIZATION:
  • Edit opponent files to change AI behavior
  • Modify game_engine.py for custom rules
  • Adjust UI colors in game_ui.py
  • Add new game modes by extending GameMode enum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Good luck, champion! May your victories be many and your Elo rating rise ever higher.

                          ⚔️ AMALGAMATION ⚔️
                    Where AI Meets Competition

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
