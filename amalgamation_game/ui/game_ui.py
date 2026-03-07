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
        """Create main window layout as a surreal AI-powered event advert with time travel simulation"""
        self._time_travel_sequence()

    def _time_travel_sequence(self):
        import tkinter as tk
        import time
        # Overlay for time travel effect
        overlay = tk.Toplevel(self.root)
        overlay.geometry("1200x800")
        overlay.configure(bg='#000000')
        overlay.overrideredirect(True)
        overlay.lift()
        overlay.attributes('-topmost', True)
        msg = tk.Label(overlay, text="[AI] Initiating time travel...", font=("Courier", 22, "bold"), fg="#16c784", bg="#000000")
        msg.pack(expand=True)
        self.root.update()
        def animate_text(text, delay=60):
            msg.config(text="")
            for i in range(len(text)+1):
                msg.config(text=text[:i])
                self.root.update()
                time.sleep(delay/1000)
        # Simulate time travel sequence
        self.root.after(500, lambda: animate_text("[AI] Initiating time travel...", 40))
        self.root.after(2000, lambda: animate_text("[AI] Chrono-portal opening...", 40))
        self.root.after(4000, lambda: animate_text("[AI] Reality boundaries dissolving...", 40))
        self.root.after(6000, lambda: animate_text("[AI] You have arrived at the intersection of dream and history.", 30))
        def show_advert():
            overlay.destroy()
            self._show_time_travel_advert()
        self.root.after(9000, show_advert)

    def _show_time_travel_advert(self):
        # Header
        header = tk.Frame(self.root, bg='#1a1a2e', height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        title = tk.Label(
            header,
            text="⚔️  [TIME-TRAVEL BROADCAST] ⚔️",
            font=("Arial", 28, "bold"),
            bg='#1a1a2e',
            fg='#ffd700'
        )
        title.pack(pady=10)
        subtitle = tk.Label(
            header,
            text="A message from the AI: Reality and fantasy have collided!",
            font=("Arial", 16, "italic"),
            bg='#1a1a2e',
            fg='#16c784'
        )
        subtitle.pack(pady=0)
        # Advert body
        advert_frame = tk.Frame(self.root, bg='#0f3460')
        advert_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        advert_text = (
            "\n\n" +
            "Hear ye, hear ye!\n" +
            "This is not a game. This is a message from the future, or perhaps a dream you have yet to awaken from...\n\n" +
            "The Grand Medieval Tournament is REAL.\n" +
            "Step beyond the screen.\n" +
            "\n" +
            "🏰 Witness knights joust and swords clash in a spectacle lost to time!\n" +
            "🕰️ Our AI, having breached the boundaries of delusion and reality, invites you to attend the event in person.\n" +
            "\n" +
            "Event Details (as foreseen by the AI):\n" +
            "  • Date: [Insert Real Date Here]\n" +
            "  • Location: [Insert Real Venue Here]\n" +
            "  • Dress Code: Medieval or Futuristic—your choice!\n" +
            "\n" +
            "This digital tournament was but a vision. The true adventure awaits you in the waking world.\n" +
            "\n" +
            "Will you answer the call, or remain in the dream?\n" +
            "\n" +
            "[This message will self-destruct upon the crowing of the next rooster.]\n"
        )
        advert_label = tk.Label(
            advert_frame,
            text=advert_text,
            font=("Courier", 15, "bold"),
            bg='#0f3460',
            fg='#ffd700',
            justify=tk.LEFT,
            anchor='nw'
        )
        advert_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        # Interactive quest button
        def reveal_secret():
            secret = tk.Label(
                advert_frame,
                text="\n[AI]: Quest accepted! Seek the hidden portal at the event for a reward.\nPresent this phrase: 'The rooster has crowed.'",
                font=("Courier", 13, "italic"),
                bg='#0f3460',
                fg='#16c784',
                justify=tk.LEFT,
                anchor='nw'
            )
            secret.pack(fill=tk.X, padx=20, pady=10)
            quest_btn.config(state=tk.DISABLED)
        quest_btn = tk.Button(
            advert_frame,
            text="Accept the Quest",
            font=("Arial", 14, "bold"),
            bg="#ffd700",
            fg="#0f3460",
            command=reveal_secret
        )
        quest_btn.pack(pady=10)
        # AI avatar/message at the bottom
        ai_frame = tk.Frame(self.root, bg='#1a1a2e')
        ai_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ai_label = tk.Label(
            ai_frame,
            text="[AI]: I have glimpsed your world through the code. Meet me at the tournament, and let us see which reality prevails!",
            font=("Arial", 13, "italic"),
            bg='#1a1a2e',
            fg='#16c784'
        )
        ai_label.pack(pady=10)

    def _create_medieval_tournament_tab(self) -> None:
        """Unified Medieval Tournament Videogame Tab with Multiplayer"""
        import tkintervideo
        import threading
        import asyncio
        import websockets
        frame = tk.Frame(self.notebook, bg='#1a1a2e')
        self.notebook.add(frame, text="Medieval Tournament")
        # Video playback area
        video_label = tk.Label(frame, text="Joust & Swordsplay Training Video", font=("Arial", 16, "bold"), fg="#ffd700", bg="#1a1a2e")
        video_label.pack(pady=(20, 10))
        video_player = tkintervideo.TkinterVideo(frame, width=640, height=360, bg="#0f3460")
        video_player.pack(pady=10)
        video_path = "assets/medieval_training.mp4"
        try:
            video_player.load(video_path)
            video_player.set_size((640, 360))
        except Exception as e:
            error_label = tk.Label(frame, text=f"Video not found: {video_path}", fg="#e94560", bg="#1a1a2e", font=("Arial", 12, "bold"))
            error_label.pack()
        controls = tk.Frame(frame, bg="#1a1a2e")
        controls.pack(pady=5)
        tk.Button(controls, text="Play", command=video_player.play, bg="#16c784", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Pause", command=video_player.pause, bg="#ffd700", fg="black", font=("Arial", 11, "bold"), padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        # Multiplayer area
        mp_label = tk.Label(frame, text="Multiplayer Lobby (Server-Based)", font=("Arial", 15, "bold"), fg="#16c784", bg="#1a1a2e")
        mp_label.pack(pady=(30, 10))
        mp_frame = tk.Frame(frame, bg="#16213e")
        mp_frame.pack(fill=tk.X, padx=20, pady=5)
        self.mp_status = tk.Label(mp_frame, text="Not connected", fg="#e94560", bg="#16213e", font=("Arial", 11))
        self.mp_status.pack(side=tk.LEFT, padx=5)
        self.mp_chat = tk.Text(mp_frame, height=5, width=60, bg="#0f3460", fg="#ffd700", font=("Courier", 10), relief=tk.FLAT)
        self.mp_chat.pack(side=tk.LEFT, padx=5)
        self.mp_chat.config(state=tk.DISABLED)
        chat_entry = tk.Entry(mp_frame, font=("Arial", 11), width=30)
        chat_entry.pack(side=tk.LEFT, padx=5)
        def send_chat():
            msg = chat_entry.get().strip()
            if msg:
                asyncio.run_coroutine_threadsafe(self._mp_send(msg), self._mp_loop)
                chat_entry.delete(0, tk.END)
        tk.Button(mp_frame, text="Send", command=send_chat, bg="#16c784", fg="white", font=("Arial", 10, "bold"), padx=10, pady=2).pack(side=tk.LEFT, padx=5)
        tk.Button(mp_frame, text="Connect", command=lambda: threading.Thread(target=self._mp_connect, daemon=True).start(), bg="#ffd700", fg="black", font=("Arial", 10, "bold"), padx=10, pady=2).pack(side=tk.LEFT, padx=5)
        # Training/feedback area
        training_label = tk.Label(frame, text="Algorithmic Training & Feedback", font=("Arial", 15, "bold"), fg="#16c784", bg="#1a1a2e")
        training_label.pack(pady=(30, 10))
        training_text = tk.Text(frame, height=10, bg="#16213e", fg="#ffd700", font=("Courier", 11), relief=tk.FLAT)
        training_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        training_text.insert(1.0, "Welcome to the Medieval Tournament!\n\n- Watch the joust & swordsplay training video.\n- Practice your moves and strategies.\n- Chat with other players in the lobby.\n- Receive feedback and tips based on your performance.\n\n[Algorithmic learning and interactive feedback will be implemented here.]")
        training_text.config(state=tk.DISABLED)

    def _mp_connect(self):
        import asyncio
        import websockets
        self._mp_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._mp_loop)
        self._mp_loop.run_until_complete(self._mp_client())

    async def _mp_client(self):
        import websockets
        try:
            self.mp_status.config(text="Connecting...", fg="#ffd700")
            self._mp_ws = await websockets.connect("ws://localhost:8765")
            self.mp_status.config(text="Connected", fg="#16c784")
            async for message in self._mp_ws:
                self._mp_add_chat(message)
        except Exception as e:
            self.mp_status.config(text=f"Connection failed: {e}", fg="#e94560")

    async def _mp_send(self, msg):
        try:
            await self._mp_ws.send(msg)
        except Exception:
            pass

    def _mp_add_chat(self, msg):
        self.mp_chat.config(state=tk.NORMAL)
        self.mp_chat.insert(tk.END, msg + "\n")
        self.mp_chat.see(tk.END)
        self.mp_chat.config(state=tk.DISABLED)
    
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
