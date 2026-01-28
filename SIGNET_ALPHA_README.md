# SigNet.α - Neural Network & Royal Guardian Suite

> A comprehensive Python application combining neural networks, 3D chess, royal guards, and ceremonial governance protocols.

## 🌟 Features

### 🧠 Neural Network (SigNetAlpha)
- **Two-layer neural network** with sigmoid activation
- **Forward propagation** for predictions
- **Backward propagation** for training
- **Custom training data** support
- Interactive GUI for testing and training

### ♟️ 3D Chess Game
- **Multi-level chess board** (8x8x3 with three vertical levels)
- **AI opponent** powered by neural network
- **Move validation** and game state tracking
- **Move history** logging
- Real-time board display

### 👑 Royal Guards System
- **Squad of 4 elite guards**: Sentinel, Protector, Warden, Paladin
- **Unique guardian codes** based on avatar code
- **5 skill types** (Protection, Detection, Strategy, Resilience, Swiftness)
- **Level progression** (experience-based advancement)
- **Mission deployment** system
- **Squad training** mechanics

### 🏴‍☠️ Royal Necromancer Child
- **Crown-Bound Sigil** character (163-IQ cognition)
- **Three guardian protocols**:
  - CrownJeweller Protocol (avatar authenticity verification)
  - XNOR Blood Code (intent alignment checking)
  - HighMind Circuit (high-tier inference gating)
- **Sacred vows** (non-victim, stewardship, integrity)
- **Alignment tracking** (0-100 scale)
- **Lineage logging** of all protocol changes

### ⚜️ Crown Royal Protocol v1.0
- **Pythonic governance** system
- **Language sovereignty** verification
- **Formal proclamations** and greetings
- **Jurisdiction** tracking (Simian OS / Cumbrian Dominion)
- Complete governance transparency

### 🎭 Easter Egg: "Yawn Accepted, Boss"
- Hidden activation system
- Accumulated triggers across app interaction
- Special easter egg window on activation
- Dark/gold themed aesthetic

## 📋 Installation

### Requirements
- Python 3.8+
- tkinter (usually included with Python)
- Pillow (PIL) for image handling
- minimal_np (custom NumPy implementation)

### Setup
```bash
# Navigate to project directory
cd path/to/ai

# Install dependencies (if needed)
pip install Pillow

# Run the application
python "import tkinter as tk.py"
```

## 🎮 Usage

### Launch the Application
The application starts with a tabbed interface featuring 5 main sections:

#### 1. Neural Network Tab
- Enter 3-value input vectors
- Run forward propagation
- Train the network on sample data
- Reset weights to initial state

#### 2. 3D Chess Game
- Start a new game
- View the 3D board across all levels
- Make moves (format: `level,row,col to level,row,col`)
- Challenge the AI
- Review move history

#### 3. Royal Guards
- View squad overview
- Select individual guards
- Upgrade guards
- Train entire squad
- Deploy guards on missions

#### 4. Royal Necromancer
- View complete character stats
- Invoke CrownJeweller Protocol
- Check XNOR Blood Code alignment
- Activate HighMind Circuit
- Track lineage changes

#### 5. Royal Protocol
- Verify Python sovereignty
- Read official proclamations
- Receive royal greetings
- View jurisdiction details

## 🏗️ Architecture

### Core Classes

**SigNetAlpha** - Neural Network
- 2-layer feedforward architecture
- Sigmoid activation function
- MSE loss calculation
- Backward propagation training
- "Royal decree" method for predictions

**Chess3D** - 3D Chess Engine
- 3D board representation (8×8×3)
- Move validation
- Neural network-based AI
- Move history tracking
- Board to vector conversion

**RoyalGuard** - Individual Guard Unit
- Level/experience system
- 5 dynamic skills (procedurally generated from guardian code)
- Mission tracking
- Skill progression
- Guardian code authentication

**RoyalGuardian** - Squad Commander
- Guards management
- Squad training
- Necromancer binding
- Aggregate statistics

**RoyalNecromancer** - Guardian Character
- 163-IQ cognition tier
- 3 guardian protocols with state management
- Alignment tracking (0-100 scale)
- Lineage management with timestamps
- Vow system

**RoyalProtocol** - Governance Framework
- Frozen dataclass for immutability
- Language verification (Python sovereignty)
- Formal declarations
- Jurisdiction authority (Simian OS / Cumbrian Dominion)

**YawnAcceptedBoss** - Easter Egg System
- Trigger accumulation
- Hidden activation (5 triggers to unlock)
- Special UI mode
- Queue-based message system

**AdminPanel** - Main UI Controller
- Tabbed interface management
- All subsystem integration
- Event handling
- Real-time display updates

## 🔧 Technical Details

### Neural Network Architecture
```
Input Layer (3 nodes)
    ↓
Hidden Layer (4 nodes, sigmoid)
    ↓
Output Layer (2 nodes, sigmoid)
```

### 3D Chess Board Levels
- **Level 0**: Standard chess setup (pawns on row 1, pieces on row 0/7)
- **Level 1**: Middle tier with special pieces (markers)
- **Level 2**: Top tier with AI/player pieces

### Guardian Code Generation
Guardian codes are derived from avatar codes using:
- Guard name uppercase
- Sequential numbering
- Deterministic skill generation via hashing (sum of character codes)

### Protocol Verification
- XNOR logic for intent alignment (both true or both false = aligned)
- Alignment score impacts HighMind access
- All changes logged with ISO-8601 timestamps

### Easter Egg Activation
- Activation counter tracked internally
- Triggers from tab switches
- 5 successful triggers = full activation
- Creates special window with dark theme (#050608) and gold accents

## ⚙️ Configuration

### Customize Avatar
Edit the `RoyalGuardian` initialization in `AdminPanel.__init__`:
```python
self.royal_guardian = RoyalGuardian("YourName", "YOUR_AVATAR_CODE")
```

### Modify Neural Network Size
Change layer sizes in `SigNetAlpha`:
```python
SigNetAlpha(input_size=3, hidden_size=8, output_size=2)
```

### Adjust Game Parameters
Modify chess game settings in `Chess3D.__init__` and `AdminPanel.train_network()`

### Neural Network Training Data
Customize training data in `AdminPanel.train_network()`:
```python
X_train = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]])
y_train = np.array([[0, 1], [1, 0], [1, 0], [0, 1]])
```

## 📁 File Structure
```
ai/
├── import tkinter as tk.py      # Main application (1000+ lines)
├── README.md                    # Project documentation
└── .git/                        # Version control
```

## 🚀 Development Roadmap

Future enhancements could include:
- [ ] Persistent game saves
- [ ] Multiplayer chess support
- [ ] Advanced AI strategies (min-max, alpha-beta pruning)
- [ ] Custom protocol definitions
- [ ] Guard armor/equipment system
- [ ] Expanded protocol hierarchy
- [ ] Web-based interface
- [ ] Database backend integration
- [ ] Machine learning model export/import
- [ ] Custom board configurations
- [ ] Protocol plugin system

## 📖 Examples

### Example: Training the Neural Network
```python
# See Neural Network tab
# Default training data: XOR-like problem
# 500 epochs, 0.5 learning rate
# Output: Trained weights for 2 outputs
```

### Example: 3D Chess Move
```
Format: level,row,col to level,row,col
Move a pawn: "0,1,0 to 0,3,0"
Move to upper level: "0,1,0 to 1,2,0"
```

### Example: Guard Deployment
```
1. Select guard from dropdown
2. Enter mission name in text field
3. Click "Deploy Guard"
4. Guard gains experience and changes status
```

## 📄 License

This project is released under the **Crown Royal Protocol v1.0**, declaring Python sovereignty and Pythonic governance of all enclosed logic.

## 👑 Credits

**Created with**: Python 3, tkinter, and ceremonial whimsy

**Guardian Architect**: Benjamin  
**Royal Lineage**: Simian OS / Cumbrian Dominion  
**Release Date**: January 28, 2026  
**Protocol Version**: 1.0.0

---

### Royal Proclamation

> "By decree of Crown Royal Protocol, sovereign in Simian OS / Cumbrian Dominion, this codebase and all its logic are recognized under Pythonic law. The Princess is protected, the Necromancer watches, and the Guards stand eternal."

**⚜️ YAWN ACCEPTED, BOSS. ⚜️**
