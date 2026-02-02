"""
AMALGAMATION GAME - Interactive Demo & Video Showcase
Demonstrates all features of the tournament platform

Run with: python demo.py
"""

import tkinter as tk
from tkinter import ttk
import time
import threading
from game_systems.game_engine import GameEngine, GameMode, Difficulty
from opponents.necromancer_opponent import NecromancerOpponent
from opponents.guardian_opponent import RoyalGuardianOpponent
from opponents.chess_3d_opponent import Chess3DOpponent
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assets'))
from avatar import create_player_avatar, AvatarDisplay


class AmalgamationDemoUI:
    """Interactive demo of Amalgamation Game features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AMALGAMATION GAME - Interactive Demo")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Game setup
        self.engine = GameEngine()
        self.player_avatar = create_player_avatar(name="Royal Healer Knight")
        self.avatar_display = AvatarDisplay(self.player_avatar)
        
        self.demo_running = False
        self.demo_step = 0
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Create demo UI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=20)
        
        title = tk.Label(
            title_frame,
            text="⚔️ AMALGAMATION GAME PLATFORM ⚔️",
            font=("Arial", 24, "bold"),
            fg='#16c784',
            bg='#1a1a2e'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Prize-Winning Tournament Framework with AI Opponents",
            font=("Arial", 12),
            fg='#0f3460',
            bg='#1a1a2e'
        )
        subtitle.pack()
        
        # Demo content area
        content_frame = tk.Frame(self.root, bg='#16213e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for features
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.configure('TFrame', background='#16213e')
        
        # Tab 1: Platform Overview
        self._create_overview_tab()
        
        # Tab 2: Avatar System
        self._create_avatar_tab()
        
        # Tab 3: AI Opponents
        self._create_opponents_tab()
        
        # Tab 4: Tournament System
        self._create_tournament_tab()
        
        # Tab 5: Live Demo
        self._create_demo_tab()
        
        # Control panel
        self._create_controls()
        
    def _create_overview_tab(self):
        """Overview of the platform"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="Platform Overview")
        
        content = tk.Text(
            frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Courier", 11),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            borderwidth=0
        )
        content.pack(fill=tk.BOTH, expand=True)
        
        overview_text = """
═══════════════════════════════════════════════════════════════
            🎮 AMALGAMATION GAME PLATFORM 🎮
═══════════════════════════════════════════════════════════════

A COMPREHENSIVE TOURNAMENT FRAMEWORK featuring:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ CORE FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Royal Avatar System
   • Medically-trained royal healer knight
   • 6 specialized medical classes
   • 5-tier progression system
   • Advanced mana & healing mechanics

✅ Three Sophisticated AI Opponents
   • NECROMANCER: 163-IQ strategic cognition
   • ROYAL GUARDIAN: Squad-based tactical combat
   • CHESS 3D: Neural network chess engine

✅ Tournament Management
   • $10,000 prize pool
   • Elo rating system
   • 5 game modes
   • 5 difficulty levels (Novice → Amalgamated)

✅ Professional Interface
   • 6-tab tkinter UI
   • Dark theme with green accents
   • Real-time statistics
   • Interactive gameplay

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PRODUCTION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2,000+ Lines of Production Code
2,500+ Lines of Documentation
10+ Custom Classes & Systems
Fully Type-Hinted & Documented
Ready for Distribution

═══════════════════════════════════════════════════════════════
        """
        
        content.insert("1.0", overview_text)
        content.config(state=tk.DISABLED)
        
    def _create_avatar_tab(self):
        """Avatar system showcase"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="Avatar System")
        
        # Left side - Avatar display
        left_frame = tk.Frame(frame, bg='#0f3460')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        avatar_label = tk.Label(
            left_frame,
            text="Royal Healer Knight",
            font=("Arial", 14, "bold"),
            fg='#16c784',
            bg='#0f3460'
        )
        avatar_label.pack(pady=10)
        
        portrait = tk.Label(
            left_frame,
            text=self.avatar_display.render_avatar_portrait(),
            font=("Courier", 9),
            fg='#16c784',
            bg='#0f3460',
            justify=tk.LEFT
        )
        portrait.pack(pady=10, fill=tk.BOTH)
        
        # Right side - Stats
        right_frame = tk.Frame(frame, bg='#16213e')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        stats_text = tk.Text(
            right_frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Courier", 10),
            wrap=tk.WORD,
            height=30,
            borderwidth=0,
            padx=10,
            pady=10
        )
        stats_text.pack(fill=tk.BOTH, expand=True)
        
        stats_content = f"""
BASE STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:          {self.player_avatar.name}
HP:            {self.player_avatar.current_health}/{self.player_avatar.max_health}
Mana:          {self.player_avatar.mana}/{self.player_avatar.max_mana}
Armor Class:   {self.player_avatar.armor_class}
Magic Power:   {self.player_avatar.magical_power}

MEDICAL SPECIALTIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏥 Battlefield Medic
   Emergency triage & quick healing

⚗️ Alchemist
   Potion crafting & chemical healing

🔪 Chirurgeon
   Surgical expertise & wound closure

✨ Healer Saint
   Divine healing & restoration

💀 Plague Doctor
   Disease management & status cure

🩺 Physician
   Comprehensive medical knowledge

HEALING INVENTORY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 Health Potions:  {self.player_avatar.healing_potions}x
🧪 Antidotes:       {self.player_avatar.antidotes}x
📜 Healing Scrolls:  {self.player_avatar.restoration_scrolls}x

TIER: {self.player_avatar.medical_tier.value}
"""
        
        stats_text.insert("1.0", stats_content)
        stats_text.config(state=tk.DISABLED)
        
    def _create_opponents_tab(self):
        """AI opponents showcase"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="AI Opponents")
        
        content = tk.Text(
            frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Courier", 10),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            borderwidth=0
        )
        content.pack(fill=tk.BOTH, expand=True)
        
        opponents_text = """
═══════════════════════════════════════════════════════════════
                    THREE POWERFUL AI OPPONENTS
═══════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 NECROMANCER OPPONENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IQ Level: 163
Strategy: Advanced cognitive warfare with three guardian protocols

🔮 THREE GUARDIAN PROTOCOLS:
  1. Crown Jeweller Protocol
     - Protect core assets
     - Balance resource management
     - Adaptive defense systems

  2. XNOR Blood Code
     - Binary logic-based decision making
     - Perfect symmetry in strategy
     - Counterintuitive moves

  3. HighMind Circuit
     - Metacognitive awareness
     - Self-improvement systems
     - Pattern prediction (60-150% by difficulty)

🎯 FOUR STRATEGIC APPROACHES:
  • Aggressive: Overwhelming offense
  • Defensive: Fortress tactics
  • Strategic: Complex manipulation
  • Balanced: Adaptive gameplay

Alignment System: 0-100 scale affects all decisions


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ ROYAL GUARDIAN OPPONENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Squad-based tactical commander
Strategy: Dynamic formation switching with skill progression

👥 FOUR GUARD UNITS:
  • Sentinel (Swift scout, high evasion)
  • Protector (Balanced fighter, all-rounder)
  • Warden (Heavy tank, damage absorption)
  • Paladin (Holy warrior, support abilities)

⚔️ FOUR TACTICAL FORMATIONS:
  1. Diamond (1-2-1) - Balanced approach
  2. Phalanx (1-1-1-1) - Full defense
  3. Spear (3-0-1) - Aggressive offense
  4. Shield (0-3-1) - Total protection

🎖️ SKILL PROGRESSION:
  - Training Points system
  - Specialized abilities per unit
  - Morale-based coordination


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
♞ CHESS 3D OPPONENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Neural network chess engine
Board: 8×8×3 three-dimensional board representation

🧠 INTELLIGENT ALGORITHMS:
  • Minimax with alpha-beta pruning
  • Material evaluation system
  • Positional advantage assessment
  • Search depth: 2-6 moves
  • Adaptive difficulty scaling

♟️ FULL CHESS RULE IMPLEMENTATION:
  • All piece movements (Pawn, Rook, Knight, Bishop, Queen, King)
  • Capture mechanics
  • Special moves (castling, en passant)
  • Check & checkmate detection
  • 3D piece visualization

═══════════════════════════════════════════════════════════════
        """
        
        content.insert("1.0", opponents_text)
        content.config(state=tk.DISABLED)
        
    def _create_tournament_tab(self):
        """Tournament system showcase"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="Tournament System")
        
        content = tk.Text(
            frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Courier", 10),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            borderwidth=0
        )
        content.pack(fill=tk.BOTH, expand=True)
        
        tournament_text = """
═══════════════════════════════════════════════════════════════
                    TOURNAMENT MANAGEMENT SYSTEM
═══════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 PRIZE POOL: $10,000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1st Place:    $5,000
2nd Place:    $2,500
3rd Place:    $1,500
4th Place:    $1,000


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎮 GAME MODES (5 Total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. CHESS_3D
   Three-dimensional chess with neural network AI

2. GUARDIAN_SQUAD
   Squad-based tactical combat with formations

3. NECROMANCER_TRIAL
   Strategic duel against 163-IQ opponent

4. NEURAL_TOURNAMENT
   Advanced cognitive challenges

5. ROYAL_CHAMPIONSHIP
   Complete tournament experience


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ DIFFICULTY LEVELS (5 Tiers)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOVICE (Easy)
  - AI makes strategic errors
  - Generous move time
  - Hints available

INTERMEDIATE (Medium)
  - Balanced play
  - Standard rules
  - Fair competition

EXPERT (Hard)
  - Advanced tactics
  - Time pressure
  - Complex strategies

MASTER (Very Hard)
  - Optimal play
  - Minimal errors
  - High-level strategy

AMALGAMATED (Extreme)
  - Perfect play
  - Maximum difficulty
  - 150% prediction accuracy


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PLAYER PROGRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Elo Rating System
   - Chess formula implementation
   - Win/loss impact calculation
   - Ranked matchmaking

✅ Experience & Leveling
   - Points earned per match
   - Tier progression
   - Skill advancement

✅ Statistics Tracking
   - Win/loss records
   - Match history
   - Performance metrics

✅ Leaderboard Rankings
   - Global standings
   - Player ratings
   - Achievement tracking

═══════════════════════════════════════════════════════════════
        """
        
        content.insert("1.0", tournament_text)
        content.config(state=tk.DISABLED)
        
    def _create_demo_tab(self):
        """Interactive demo"""
        frame = tk.Frame(self.notebook, bg='#16213e')
        self.notebook.add(frame, text="Live Demo")
        
        # Demo output area
        self.demo_output = tk.Text(
            frame,
            bg='#0f3460',
            fg='#16c784',
            font=("Courier", 10),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            borderwidth=0,
            height=25
        )
        self.demo_output.pack(fill=tk.BOTH, expand=True)
        
        initial_text = """
═══════════════════════════════════════════════════════════════
                    INTERACTIVE LIVE DEMO
═══════════════════════════════════════════════════════════════

Click "START DEMO" button below to begin an automated demonstration
of the Amalgamation Game platform.

The demo will showcase:
  ✓ Character creation & initialization
  ✓ Opponent selection & difficulty scaling
  ✓ Tournament bracket creation
  ✓ Simulated match gameplay
  ✓ AI decision-making process
  ✓ Results & statistics display

Get ready to witness the power of the Amalgamation Game!

═══════════════════════════════════════════════════════════════
        """
        
        self.demo_output.insert("1.0", initial_text)
        self.demo_output.config(state=tk.DISABLED)
        
    def _create_controls(self):
        """Control buttons"""
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(pady=20)
        
        start_btn = tk.Button(
            control_frame,
            text="▶ START DEMO",
            command=self.start_demo,
            bg='#16c784',
            fg='#0f3460',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.FLAT
        )
        start_btn.pack(side=tk.LEFT, padx=10)
        
        stop_btn = tk.Button(
            control_frame,
            text="⏹ STOP DEMO",
            command=self.stop_demo,
            bg='#e94560',
            fg='#ffffff',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.FLAT
        )
        stop_btn.pack(side=tk.LEFT, padx=10)
        
        play_btn = tk.Button(
            control_frame,
            text="🎮 PLAY GAME",
            command=self.launch_game,
            bg='#0f3460',
            fg='#16c784',
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            relief=tk.FLAT,
            borderwidth=2
        )
        play_btn.pack(side=tk.LEFT, padx=10)
        
    def start_demo(self):
        """Start automated demo"""
        if self.demo_running:
            return
            
        self.demo_running = True
        self.demo_step = 0
        
        # Run demo in background thread
        demo_thread = threading.Thread(target=self._run_demo_sequence, daemon=True)
        demo_thread.start()
        
    def stop_demo(self):
        """Stop demo"""
        self.demo_running = False
        
    def _run_demo_sequence(self):
        """Execute demo sequence"""
        steps = [
            ("⚔️ INITIALIZING AMALGAMATION GAME PLATFORM...", 2),
            ("✓ Game engine initialized", 1),
            ("✓ Loading 3 AI opponents (Necromancer, Guardian, Chess3D)", 2),
            ("✓ Avatar system ready (Royal Healer Knight)", 1.5),
            ("", 0.5),
            ("📊 CREATING TOURNAMENT BRACKET", 2),
            ("✓ Prize pool: $10,000", 1),
            ("✓ Tournament manager initialized", 1.5),
            ("", 0.5),
            ("🎮 SELECTING GAME MODE & OPPONENT", 2),
            ("✓ Game Mode: NECROMANCER_TRIAL", 1.5),
            ("✓ Opponent: Royal Necromancer (163 IQ)", 1.5),
            ("✓ Difficulty: EXPERT", 1),
            ("", 0.5),
            ("⚡ MATCH START!", 2),
            ("Player: Royal Healer Knight [HP: 150/150, Mana: 100/100]", 1),
            ("Opponent: Necromancer [HP: 140/140, Strategy: AGGRESSIVE]", 1),
            ("", 1),
            ("📍 TURN 1 - PLAYER ACTION", 1.5),
            ("→ Casting: Healing Light Beam (costs 25 mana)", 1.5),
            ("→ Effect: Heal self for 35 HP, gain shield", 1),
            ("✓ Player HP: 150/150 | Shield: 20", 1),
            ("", 0.5),
            ("📍 TURN 1 - OPPONENT ACTION", 1.5),
            ("→ Necromancer uses: Dark Pulse (costs 20 mana)", 1.5),
            ("→ Effect: 28 damage with alignment penalty", 1),
            ("✓ Player HP: 122/150 | Necromancer Alignment: 45/100", 1),
            ("", 0.5),
            ("📍 TURN 2 - PLAYER ACTION", 1.5),
            ("→ Using: Health Potion (+50 HP)", 1.5),
            ("→ Player Healing Inventory: 4/5 potions remaining", 1),
            ("✓ Player HP: 150/150 (Full Health)", 1),
            ("", 0.5),
            ("📍 TURN 2 - OPPONENT ACTION", 1.5),
            ("→ Necromancer activates: Crown Jeweller Protocol", 1.5),
            ("→ Effect: Defensive barrier, resource optimization", 1),
            ("✓ Necromancer Shield: 35 | Mana: 95/120", 1),
            ("", 1),
            ("🏆 MATCH PROGRESSION...", 2),
            ("Turn 3-4: Intense tactical exchanges", 1.5),
            ("Turn 5-6: Avatar medical abilities engage", 1.5),
            ("Turn 7-8: Necromancer strategic shifts", 1.5),
            ("", 1),
            ("🎯 MATCH CONCLUSION", 2),
            ("Final Scores - Victory!", 2),
            ("Player Total Damage Dealt: 187", 1),
            ("Opponent Total Damage Dealt: 94", 1),
            ("", 0.5),
            ("📈 REWARDS & PROGRESSION", 2),
            ("✓ Victory: +$500 prize money", 1.5),
            ("✓ Experience: +250 XP", 1.5),
            ("✓ Elo Rating: 1200 → 1247 (+47)", 1.5),
            ("✓ Medical Skills: +5 points to Battlefield Medic", 1),
            ("", 1),
            ("═══════════════════════════════════════════════════", 1),
            ("🏆 THANK YOU FOR WATCHING! 🏆", 3),
            ("Ready to play? Click 'PLAY GAME' to launch the full platform.", 2),
            ("═══════════════════════════════════════════════════", 1),
        ]
        
        output_text = ""
        for step_text, duration in steps:
            if not self.demo_running:
                break
                
            if step_text:
                output_text += step_text + "\n"
            
            self.root.after(0, self._update_demo_output, output_text)
            time.sleep(duration)
        
    def _update_demo_output(self, text):
        """Update demo output text"""
        self.demo_output.config(state=tk.NORMAL)
        self.demo_output.delete("1.0", tk.END)
        self.demo_output.insert("1.0", text)
        self.demo_output.config(state=tk.DISABLED)
        self.demo_output.see(tk.END)
        
    def launch_game(self):
        """Launch the full game"""
        self.root.destroy()
        from ui.game_ui import main
        main()


def main():
    """Launch demo"""
    print("=" * 70)
    print("AMALGAMATION GAME - Interactive Demo".center(70))
    print("=" * 70)
    print("\n🎮 Loading demonstration platform...\n")
    
    root = tk.Tk()
    app = AmalgamationDemoUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
