# AMALGAMATION GAME
## Prize-Winning Competitive Game Framework

### Overview

**Amalgamation** is an advanced game engine that transforms your Signet Alpha AI systems into intelligent opponents in a professional tournament setting. The game integrates three powerful AI-driven opponents with dynamic difficulty scaling, real-time statistics tracking, and a comprehensive tournament management system.

### Features

#### 🎮 Opponent Systems

**1. Royal Necromancer (Master AI)**
- 163-IQ strategic cognition with advanced pattern recognition
- Three guardian protocols:
  - **CrownJeweller**: Resource optimization and asset management
  - **XNOR Blood Code**: Logical consistency enforcement
  - **HighMind Circuit**: High-level strategic synthesis
- Alignment-based decision making (0-100 scale)
- Four strategic archetypes:
  - Aggressive: Maximum offensive pressure
  - Defensive: Position fortification
  - Strategic: Long-term planning (5+ moves ahead)
  - Balanced: Adaptive to opponent

**2. Royal Guardian Commander (Tactical AI)**
- Squad-based tactical combat system
- Four specialized guard units:
  - **Sentinel**: Fast, agile, high mobility
  - **Protector**: Balanced stats, reliable performance
  - **Warden**: Strong defense, crowd control
  - **Paladin**: High damage output, offensive power
- Four tactical formations:
  - **Diamond**: 1-2-1 balanced approach
  - **Phalanx**: 1-1-1-1 flexible defense
  - **Spear**: 3-1 aggressive formation
  - **Shield**: 1-3 maximum defense
- Squad morale system affecting coordination
- Mission-based progression and training

**3. 3D Chess Master (Strategic AI)**
- 8×8×3 board representation with three levels
- Neural network-powered move evaluation
- Minimax algorithm with alpha-beta pruning
- Configurable search depth (2-6 moves ahead)
- Material evaluation with positional bonuses
- Capture tracking and endgame analysis

#### 🎯 Game Modes

1. **3D Chess**: Traditional chess on expanded 3D board
2. **Guardian Combat**: Tactical squad-based battle system
3. **Trial of Truth**: Narrative choice with alignment consequences
4. **Neural Duel**: Head-to-head AI reasoning competition
5. **Royal Tournament**: Multi-opponent championship bracket

#### 📊 Tournament System

- **Prize Pool**: $10,000 tournament with structured rewards
- **Difficulty Scaling**: 5 difficulty levels (Novice → Amalgamated)
- **Elo Rating System**: Dynamic player rating with K-factor = 32
- **Experience System**: Level progression with XP requirements
- **Achievement Tracking**: Unlockable achievements for milestones
- **Leaderboard**: Real-time tournament standings

#### 📈 Statistics & Progression

- **Player Tracking**: Wins, losses, draws, win rate
- **Elo Rating**: Competitive skill rating starting at 1600
- **Level System**: Progression through experience (500 XP per level)
- **Achievement System**: 
  - Level milestones
  - Win streaks
  - Difficulty conquests
  - Opponent mastery

#### 🎨 User Interface

**Five-Tab Interface**:
1. **Tournament**: Tournament status, prize breakdown, bracket management
2. **Select Opponent**: Opponent selection with difficulty and mode choice
3. **Gameplay**: Active match display, move execution, game controls
4. **Statistics**: Detailed player performance metrics
5. **Leaderboard**: Tournament standings and competitive rankings

**Design**: Dark theme with accent colors (#16c784 green, #e94560 red)

### Project Structure

```
amalgamation_game/
├── main.py                    # Entry point
├── game_systems/
│   ├── __init__.py
│   └── game_engine.py        # Core engine (GameEngine, OpponentAI, etc.)
├── opponents/
│   ├── __init__.py
│   ├── necromancer_opponent.py  # 163-IQ strategic AI
│   ├── guardian_opponent.py     # Squad-based tactical AI
│   └── chess_3d_opponent.py     # 3D chess neural network AI
├── ui/
│   ├── __init__.py
│   └── game_ui.py            # Tournament interface
├── assets/
│   └── (game resources)
└── README.md                 # This file
```

### Installation & Usage

#### Requirements
- Python 3.8+
- tkinter (included with Python)
- No external AI libraries (all neural networks built from scratch)

#### Installation
```bash
cd amalgamation_game
pip install -r requirements.txt  # If needed
python main.py
```

#### Running a Tournament
1. Launch `main.py`
2. Go to "Tournament" tab and click "Start Tournament"
3. Go to "Select Opponent" tab
4. Choose:
   - Opponent (Necromancer, Guardian, or Chess AI)
   - Difficulty (Novice → Amalgamated)
   - Game Mode (3D Chess, Guardian Combat, etc.)
5. Click "START MATCH"
6. Execute moves against the AI opponent
7. Click "End Game" to finish and record result
8. Check "Statistics" and "Leaderboard" tabs for progress

### AI Opponent Analysis

#### Necromancer Algorithm
```
Input: Player Move
  ↓
[1] HighMind Circuit: Pattern Analysis (163-IQ cognition)
  ↓
[2] Protocol Invocation: Resource/Logic/Strategy decisions
  ↓
[3] Strategy Execution: Aggr/Def/Strat/Balanced approaches
  ↓
[4] Alignment Filter: Modify confidence based on alignment
  ↓
Output: Strategic Move with confidence scoring
```

#### Guardian Algorithm
```
Input: Player Move
  ↓
[1] Threat Assessment: Evaluate attack intensity
  ↓
[2] Formation Selection: Choose optimal defensive/offensive setup
  ↓
[3] Guard Assignment: Position 4 guards in formation
  ↓
[4] Squad Coordination: Execute unified attack/defense
  ↓
Output: Tactical action with squad morale factor
```

#### Chess 3D Algorithm
```
Input: Player Move
  ↓
[1] Board Update: Apply move to 8×8×3 representation
  ↓
[2] Legal Move Generation: Find all valid AI moves
  ↓
[3] Minimax Evaluation: Search to configured depth
  ↓
[4] Material + Position: Evaluate captures and positions
  ↓
Output: Highest-scored move with evaluation metric
```

### Difficulty Levels & Scaling

| Difficulty | Elo Multiplier | Necromancer Strategy | Guardian Health | Chess Depth |
|-----------|----------------|-------------------|-----------------|------------|
| Novice | 0.5x | Defensive | 70% | 2 |
| Adept | 1.0x | Balanced | 100% | 3 |
| Master | 1.5x | Strategic | 130% | 4 |
| Legendary | 2.0x | Aggressive | 160% | 5 |
| Amalgamated | 3.0x | Max Aggressive | 200% | 6 |

### Prize Structure

```
Tournament: $10,000 Prize Pool
├─ 1st Place (Champion): $5,000
├─ 2nd Place (Runner-up): $3,000
├─ 3rd Place (Finalist): $2,000
└─ 4th Place: $1,000
```

### Elo Rating System

Standard chess Elo calculation with K-factor = 32:
- Expected Score = 1 / (1 + 10^((opponent_elo - player_elo) / 400))
- New Rating = Old Rating + K × (Score - Expected)
- Win = 1 point, Draw = 0.5, Loss = 0

### Future Enhancements

- [ ] Neural network-based player move prediction
- [ ] Persistent game save system
- [ ] Multiplayer online tournament support
- [ ] Advanced AI with deep reinforcement learning
- [ ] Custom tournament creation and bracket management
- [ ] Replay system with move analysis
- [ ] Voice commentary integration
- [ ] VR/3D visualization for chess board

### Technical Details

**Code Stats**:
- Game Engine: 400+ lines
- Opponent AI: 800+ lines (3 opponents)
- UI System: 600+ lines
- Total: 1,800+ lines of production-ready code

**Design Patterns Used**:
- Strategy Pattern: Opponent tactical strategies
- Factory Pattern: Opponent instantiation
- Observer Pattern: Game state updates
- Dataclass Pattern: Immutable game states
- Enum Pattern: Type-safe game modes

### License

This project is part of the Signet Alpha ecosystem.
See LICENSE file for details.

---

**AMALGAMATION** - Where AI Meets Competition 🏆⚔️
