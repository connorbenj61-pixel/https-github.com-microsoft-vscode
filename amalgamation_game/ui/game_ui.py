"""
AMALGAMATION GAME UI
Prize-Winning Game Interface

Interactive tkinter-based tournament management and gameplay
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import Optional
import sys
import os

# Add assets to path for avatar import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'assets'))

from game_systems.game_engine import (
    GameEngine, GameMode, Difficulty, TournamentManager
)
from opponents.necromancer_opponent import NecromancerOpponent
from opponents.guardian_opponent import RoyalGuardianOpponent
from opponents.chess_3d_opponent import Chess3DOpponent
from avatar import RoyalAvatar, AvatarDisplay, MedicalSpecialty, create_player_avatar


class AmalgamationGameUI:
    """
    Main GUI for Amalgamation Game
    Manages tournament, opponent selection, and gameplay
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AMALGAMATION - Prize-Winning Game")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Player avatar initialization
        self.player_avatar = create_player_avatar(name="Royal Healer Knight")
        self.avatar_display = AvatarDisplay(self.player_avatar)
        
        # Game engine initialization
        self.game_engine = GameEngine(player_name=self.player_avatar.name)
        self.tournament_manager = TournamentManager(self.game_engine)
        
        # Register opponents
        self._register_opponents()
        
        # Current game tracking
        self.current_game = None
        self.selected_opponent: Optional[str] = None
        self.selected_mode: Optional[GameMode] = None
        self.selected_difficulty: Optional[Difficulty] = None
        
        # Setup UI
        self._create_main_layout()
    
    def _register_opponents(self) -> None:
        """Register all AI opponents"""
        necromancer = NecromancerOpponent()
        guardian = RoyalGuardianOpponent()
        chess_ai = Chess3DOpponent()
        
        self.game_engine.register_opponent(necromancer)
        self.game_engine.register_opponent(guardian)
        self.game_engine.register_opponent(chess_ai)
    
    def _create_avatar_tab(self) -> None:
        """Avatar and medical system tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Avatar")
        
        # Avatar portrait display
        self.avatar_text = tk.Text(
            frame, bg='#16213e', fg='#0f3460',
            font=("Courier", 10), relief=tk.FLAT
        )
        self.avatar_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._update_avatar_display()
        self.avatar_text.config(state=tk.DISABLED)
        
        # Control buttons
        control_frame = tk.Frame(frame, bg='#1a1a2e')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            control_frame, text="Cast Healing Spell",
            bg='#16c784', fg='white', font=("Arial", 10, "bold"),
            command=self._cast_healing_spell,
            relief=tk.FLAT, padx=15, pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="Use Potion",
            bg='#ffd700', fg='black', font=("Arial", 10, "bold"),
            command=self._use_potion,
            relief=tk.FLAT, padx=15, pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="Upgrade Medical Tier",
            bg='#a78bfa', fg='white', font=("Arial", 10, "bold"),
            command=self._upgrade_medical_tier,
            relief=tk.FLAT, padx=15, pady=8
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="Refresh",
            bg='#0f3460', fg='#16c784', font=("Arial", 10, "bold"),
            command=self._update_avatar_display,
            relief=tk.FLAT, padx=15, pady=8
        ).pack(side=tk.LEFT, padx=5)
    
    def _update_avatar_display(self) -> None:
        """Update avatar portrait display"""
        self.avatar_text.config(state=tk.NORMAL)
        self.avatar_text.delete(1.0, tk.END)
        
        portrait = self.avatar_display.render_avatar_portrait()
        self.avatar_text.insert(1.0, portrait)
        
        self.avatar_text.config(state=tk.DISABLED)
    
    def _cast_healing_spell(self) -> None:
        """Cast healing spell"""
        abilities = list(self.player_avatar.active_specialty_abilities.keys())
        
        if not abilities:
            messagebox.showwarning("Abilities", "No abilities available")
            return
        
        # Use first ability for demo
        ability_name = abilities[0]
        result = self.player_avatar.cast_healing_spell(ability_name)
        
        if result['success']:
            messagebox.showinfo("Healing Cast", result['message'])
        else:
            messagebox.showwarning("Cast Failed", result['message'])
        
        self._update_avatar_display()
    
    def _use_potion(self) -> None:
        """Use healing potion"""
        result = self.player_avatar.use_healing_potion()
        
        if result['success']:
            messagebox.showinfo("Potion Used", result['message'])
        else:
            messagebox.showwarning("No Potions", result['message'])
        
        self._update_avatar_display()
    
    def _upgrade_medical_tier(self) -> None:
        """Upgrade medical tier"""
        if self.player_avatar.medical_tier.value >= 5:
            messagebox.showinfo("Already Maxed", "Medical tier already at maximum!")
            return
        
        self.player_avatar.upgrade_medical_specialty()
        messagebox.showinfo("Upgrade!", f"Advanced to {self.player_avatar.medical_tier.name}!")
        self._update_avatar_display()
    
    def _create_main_layout(self) -> None:
        """Create main window layout"""
        
        # Header
        header = tk.Frame(self.root, bg='#16c784', height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="⚔️  AMALGAMATION: Prize-Winning Tournament  ⚔️",
            font=("Arial", 24, "bold"),
            bg='#16c784',
            fg='white'
        )
        title.pack(pady=20)
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_avatar_tab()
        self._create_tournament_tab()
        self._create_opponent_selection_tab()
        self._create_gameplay_tab()
        self._create_stats_tab()
        self._create_leaderboard_tab()
    
    def _create_tournament_tab(self) -> None:
        """Tournament management tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Tournament")
        
        # Tournament info
        info_frame = tk.LabelFrame(
            frame, text="Tournament Status", bg='#1a1a2e', fg='#16c784',
            font=("Arial", 12, "bold")
        )
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        status_text = tk.Text(
            info_frame, height=6, bg='#16213e', fg='#0f3460',
            font=("Courier", 10), relief=tk.FLAT
        )
        status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        status_text.insert(1.0, 
            "🏆 AMALGAMATION TOURNAMENT 🏆\n\n"
            "Status: Ready for Competition\n"
            "Prize Pool: $10,000\n"
            "Registered Opponents: 3\n\n"
            "Available opponents:\n"
            "  • Royal Necromancer (Master AI)\n"
            "  • Royal Guardian Commander (Tactical AI)\n"
            "  • 3D Chess Master (Strategic AI)"
        )
        status_text.config(state=tk.DISABLED)
        
        # Controls
        control_frame = tk.Frame(frame, bg='#1a1a2e')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            control_frame, text="Start Tournament",
            bg='#16c784', fg='white', font=("Arial", 11, "bold"),
            command=self._start_tournament,
            relief=tk.FLAT, padx=15, pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="Reset Tournament",
            bg='#e94560', fg='white', font=("Arial", 11, "bold"),
            command=self._reset_tournament,
            relief=tk.FLAT, padx=15, pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Prize breakdown
        prize_frame = tk.LabelFrame(
            frame, text="Prize Breakdown", bg='#1a1a2e', fg='#16c784',
            font=("Arial", 12, "bold")
        )
        prize_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        prizes = [
            ("1st Place (Champion)", "$5,000"),
            ("2nd Place (Runner-up)", "$3,000"),
            ("3rd Place (Finalist)", "$2,000"),
            ("4th Place", "$1,000"),
        ]
        
        for place, prize in prizes:
            row = tk.Frame(prize_frame, bg='#1a1a2e')
            row.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(
                row, text=place, bg='#1a1a2e', fg='#0f3460',
                font=("Arial", 11), width=25, anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row, text=prize, bg='#1a1a2e', fg='#16c784',
                font=("Arial", 11, "bold"), width=15, anchor='e'
            ).pack(side=tk.RIGHT)
    
    def _create_opponent_selection_tab(self) -> None:
        """Opponent and difficulty selection tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Select Opponent")
        
        # Opponent selection
        opponent_frame = tk.LabelFrame(
            frame, text="Choose Your Opponent", bg='#1a1a2e', fg='#16c784',
            font=("Arial", 12, "bold")
        )
        opponent_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.opponent_var = tk.StringVar()
        
        opponents = [
            ("Royal Necromancer", "necromancer_signet"),
            ("Royal Guardian Commander", "guardian_commander"),
            ("3D Chess Master", "chess_3d_ai")
        ]
        
        for label, value in opponents:
            rb = tk.Radiobutton(
                opponent_frame, text=label, variable=self.opponent_var,
                value=value, bg='#1a1a2e', fg='#0f3460',
                selectcolor='#16c784', font=("Arial", 11),
                command=self._on_opponent_selected
            )
            rb.pack(anchor=tk.W, padx=20, pady=8)
        
        # Difficulty selection
        difficulty_frame = tk.LabelFrame(
            frame, text="Choose Difficulty", bg='#1a1a2e', fg='#16c784',
            font=("Arial", 12, "bold")
        )
        difficulty_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.difficulty_var = tk.StringVar()
        
        difficulties = [
            ("Novice", "NOVICE"),
            ("Adept", "ADEPT"),
            ("Master", "MASTER"),
            ("Legendary", "LEGENDARY"),
            ("Amalgamated", "AMALGAMATED")
        ]
        
        for label, value in difficulties:
            rb = tk.Radiobutton(
                difficulty_frame, text=label, variable=self.difficulty_var,
                value=value, bg='#1a1a2e', fg='#0f3460',
                selectcolor='#16c784', font=("Arial", 11),
                command=self._on_difficulty_selected
            )
            rb.pack(anchor=tk.W, padx=20, pady=8)
        
        # Game mode selection
        mode_frame = tk.LabelFrame(
            frame, text="Choose Game Mode", bg='#1a1a2e', fg='#16c784',
            font=("Arial", 12, "bold")
        )
        mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.mode_var = tk.StringVar()
        
        modes = [
            ("3D Chess", "chess_3d"),
            ("Guardian Combat", "guardian_combat"),
            ("Trial of Truth", "trial_of_truth"),
            ("Neural Duel", "neural_duel")
        ]
        
        for label, value in modes:
            rb = tk.Radiobutton(
                mode_frame, text=label, variable=self.mode_var,
                value=value, bg='#1a1a2e', fg='#0f3460',
                selectcolor='#16c784', font=("Arial", 11),
                command=self._on_mode_selected
            )
            rb.pack(anchor=tk.W, padx=20, pady=8)
        
        # Start button
        tk.Button(
            frame, text="START MATCH",
            bg='#16c784', fg='white', font=("Arial", 14, "bold"),
            command=self._start_match,
            relief=tk.FLAT, padx=30, pady=15
        ).pack(pady=20)
    
    def _create_gameplay_tab(self) -> None:
        """Active gameplay tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Gameplay")
        
        # Game status
        self.game_status_text = tk.Text(
            frame, height=15, bg='#16213e', fg='#0f3460',
            font=("Courier", 10), relief=tk.FLAT
        )
        self.game_status_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.game_status_text.insert(1.0, "No active game. Select opponent and start match.")
        self.game_status_text.config(state=tk.DISABLED)
        
        # Control buttons
        control_frame = tk.Frame(frame, bg='#1a1a2e')
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            control_frame, text="Execute Move",
            bg='#16c784', fg='white', font=("Arial", 11, "bold"),
            command=self._execute_move,
            relief=tk.FLAT, padx=15, pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="End Game",
            bg='#e94560', fg='white', font=("Arial", 11, "bold"),
            command=self._end_game,
            relief=tk.FLAT, padx=15, pady=10
        ).pack(side=tk.LEFT, padx=5)
    
    def _create_stats_tab(self) -> None:
        """Player statistics tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Statistics")
        
        # Stats display
        self.stats_text = tk.Text(
            frame, bg='#16213e', fg='#0f3460',
            font=("Courier", 11), relief=tk.FLAT
        )
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._update_stats_display()
    
    def _create_leaderboard_tab(self) -> None:
        """Tournament leaderboard tab"""
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Leaderboard")
        
        # Leaderboard display
        self.leaderboard_text = tk.Text(
            frame, bg='#16213e', fg='#0f3460',
            font=("Courier", 11), relief=tk.FLAT
        )
        self.leaderboard_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._update_leaderboard_display()
    
    def _on_opponent_selected(self) -> None:
        """Handle opponent selection"""
        self.selected_opponent = self.opponent_var.get()
    
    def _on_difficulty_selected(self) -> None:
        """Handle difficulty selection"""
        self.selected_difficulty = Difficulty[self.difficulty_var.get()]
    
    def _on_mode_selected(self) -> None:
        """Handle mode selection"""
        mode_str = self.mode_var.get()
        for mode in GameMode:
            if mode.value == mode_str:
                self.selected_mode = mode
                break
    
    def _start_tournament(self) -> None:
        """Initialize tournament"""
        self.tournament_manager.create_tournament(
            opponents=['necromancer_signet', 'guardian_commander', 'chess_3d_ai'],
            prize_pool=10000
        )
        messagebox.showinfo("Tournament", "Tournament initialized! Prize pool: $10,000")
    
    def _reset_tournament(self) -> None:
        """Reset tournament progress"""
        self.tournament_manager.tournament_active = False
        self.game_engine.player = self.game_engine.player.__class__(
            name=self.game_engine.player.name
        )
        messagebox.showinfo("Reset", "Tournament reset. Player stats cleared.")
    
    def _start_match(self) -> None:
        """Start match against selected opponent"""
        if not self.selected_opponent:
            messagebox.showwarning("Selection", "Please select an opponent")
            return
        
        if not self.selected_difficulty:
            messagebox.showwarning("Selection", "Please select difficulty")
            return
        
        if not self.selected_mode:
            messagebox.showwarning("Selection", "Please select game mode")
            return
        
        try:
            self.current_game = self.game_engine.start_game(
                mode=self.selected_mode,
                difficulty=self.selected_difficulty,
                opponent_id=self.selected_opponent
            )
            
            self._update_game_display()
            messagebox.showinfo("Match Started", f"Game started vs {self.game_engine.opponents[self.selected_opponent].opponent_name}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _execute_move(self) -> None:
        """Execute player move in current game"""
        if not self.current_game:
            messagebox.showwarning("Game", "No active game")
            return
        
        # Simulate player move
        player_move = {
            'type': random.choice(['attack', 'defend', 'special']),
            'aggression': random.random(),
            'defense': random.random()
        }
        
        result = self.game_engine.process_player_move(player_move)
        self._update_game_display()
    
    def _end_game(self) -> None:
        """End current game"""
        if not self.current_game:
            messagebox.showwarning("Game", "No active game")
            return
        
        # Determine winner randomly for demo
        result = random.choice(['win', 'loss', 'draw'])
        
        end_result = self.game_engine.end_game(result)
        
        messagebox.showinfo("Game Over", f"Result: {result.upper()}\nStats updated!")
        
        self.current_game = None
        self._update_stats_display()
        self._update_leaderboard_display()
    
    def _update_game_display(self) -> None:
        """Update gameplay display"""
        if not self.current_game:
            return
        
        status = self.game_engine.get_game_status()
        
        display_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                    ACTIVE MATCH DISPLAY                        ║
╚════════════════════════════════════════════════════════════════╝

Game Mode:      {status['mode'].upper()}
Difficulty:     {status['difficulty']}
Opponent:       {status['opponent']}

Round:          {status['round']}
Time Elapsed:   {status['elapsed_time']:.1f}s

Player Score:   {status['player_score']} ━━━━━━━━━
Opponent Score: {status['opponent_score']} ━━━━━━━━━

Status:         {'ACTIVE' if status['active'] else 'FINISHED'}
"""
        
        self.game_status_text.config(state=tk.NORMAL)
        self.game_status_text.delete(1.0, tk.END)
        self.game_status_text.insert(1.0, display_text)
        self.game_status_text.config(state=tk.DISABLED)
    
    def _update_stats_display(self) -> None:
        """Update player statistics display"""
        player = self.game_engine.player
        
        stats_text = f"""
╔════════════════════════════════════════════════════════════════╗
║                     PLAYER STATISTICS                          ║
╚════════════════════════════════════════════════════════════════╝

Player Name:    {player.name}
Level:          {player.level}
Experience:    {player.experience} XP

Record:
  Wins:        {player.wins}
  Losses:      {player.losses}
  Draws:       {player.draws}
  Win Rate:    {player.win_rate:.1f}%

Rating:        {player.elo_rating} Elo

Total Score:   {player.total_score}
Games Played:  {len(self.game_engine.game_history)}

Achievements:  {len(player.achievements)}
"""
        
        for achievement in player.achievements:
            stats_text += f"  ✓ {achievement}\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
    
    def _update_leaderboard_display(self) -> None:
        """Update leaderboard display"""
        lb = self.game_engine.get_leaderboard()
        
        leaderboard_text = """
╔════════════════════════════════════════════════════════════════╗
║                      TOURNAMENT LEADERBOARD                    ║
╚════════════════════════════════════════════════════════════════╝

Rank  Player               Elo      Wins    Losses
──────────────────────────────────────────────────────────────
"""
        
        for entry in lb:
            leaderboard_text += (
                f"{entry['rank']:2d}.   {entry['player']:<18s}  "
                f"{entry['elo']:<4d}    {entry['wins']:<3d}    {entry['losses']}\n"
            )
        
        self.leaderboard_text.config(state=tk.NORMAL)
        self.leaderboard_text.delete(1.0, tk.END)
        self.leaderboard_text.insert(1.0, leaderboard_text)
        self.leaderboard_text.config(state=tk.DISABLED)
    
    def run(self) -> None:
        """Start the UI"""
        self.root.mainloop()


def main():
    """Launch Amalgamation Game"""
    root = tk.Tk()
    app = AmalgamationGameUI(root)
    app.run()


if __name__ == "__main__":
    main()
