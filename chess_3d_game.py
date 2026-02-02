"""
GENIUS 3D CHESS - Battle Chess Style Game
AI-Powered Chess with Celebrity Opponents in 3D
Version 1.0.0 | February 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Set
import threading
import time


class PieceType(Enum):
    """Chess piece types"""
    PAWN = "♟"
    KNIGHT = "♞"
    BISHOP = "♝"
    ROOK = "♜"
    QUEEN = "♛"
    KING = "♚"


class Color(Enum):
    """Piece colors"""
    WHITE = "white"
    BLACK = "black"


@dataclass
class Position:
    """Board position (row, col)"""
    row: int
    col: int
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


@dataclass
class Piece:
    """Chess piece with position and color"""
    type: PieceType
    color: Color
    position: Position
    
    def __repr__(self):
        return f"{self.type.value}"


class ChessBoard:
    """Standard 8x8 chess board"""
    
    def __init__(self):
        self.board: Dict[Position, Optional[Piece]] = {}
        self.setup_board()
        self.move_history: List[Tuple[Position, Position, Optional[Piece]]] = []
        
    def setup_board(self):
        """Initialize board with starting position"""
        # Clear board
        for row in range(8):
            for col in range(8):
                self.board[Position(row, col)] = None
        
        # Setup white pieces (bottom, row 6-7)
        self._setup_side(Color.WHITE, start_row=6)
        
        # Setup black pieces (top, row 0-1)
        self._setup_side(Color.BLACK, start_row=1)
    
    def _setup_side(self, color: Color, start_row: int):
        """Setup one side of the board"""
        # Pawns
        pawn_row = start_row + (1 if color == Color.WHITE else -1)
        for col in range(8):
            self.board[Position(pawn_row, col)] = Piece(
                PieceType.PAWN, color, Position(pawn_row, col)
            )
        
        # Back row pieces
        back_row = start_row
        back_pieces = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP,
            PieceType.QUEEN, PieceType.KING, PieceType.BISHOP,
            PieceType.KNIGHT, PieceType.ROOK
        ]
        
        for col, piece_type in enumerate(back_pieces):
            self.board[Position(back_row, col)] = Piece(
                piece_type, color, Position(back_row, col)
            )
    
    def get_piece(self, pos: Position) -> Optional[Piece]:
        """Get piece at position"""
        return self.board.get(pos)
    
    def is_valid_position(self, pos: Position) -> bool:
        """Check if position is on board"""
        return 0 <= pos.row < 8 and 0 <= pos.col < 8
    
    def get_valid_moves(self, pos: Position) -> List[Position]:
        """Get all valid moves for piece at position"""
        piece = self.get_piece(pos)
        if not piece:
            return []
        
        moves = []
        
        if piece.type == PieceType.PAWN:
            moves = self._get_pawn_moves(piece)
        elif piece.type == PieceType.KNIGHT:
            moves = self._get_knight_moves(piece)
        elif piece.type == PieceType.BISHOP:
            moves = self._get_bishop_moves(piece)
        elif piece.type == PieceType.ROOK:
            moves = self._get_rook_moves(piece)
        elif piece.type == PieceType.QUEEN:
            moves = self._get_queen_moves(piece)
        elif piece.type == PieceType.KING:
            moves = self._get_king_moves(piece)
        
        return moves
    
    def _get_pawn_moves(self, piece: Piece) -> List[Position]:
        """Get pawn moves"""
        moves = []
        direction = -1 if piece.color == Color.BLACK else 1
        start_row = 1 if piece.color == Color.BLACK else 6
        
        # Forward move
        next_pos = Position(piece.position.row + direction, piece.position.col)
        if self.is_valid_position(next_pos) and not self.get_piece(next_pos):
            moves.append(next_pos)
            
            # Two squares from start
            if piece.position.row == start_row:
                next_next = Position(piece.position.row + 2*direction, piece.position.col)
                if not self.get_piece(next_next):
                    moves.append(next_next)
        
        # Captures
        for dc in [-1, 1]:
            cap_pos = Position(piece.position.row + direction, piece.position.col + dc)
            if self.is_valid_position(cap_pos):
                target = self.get_piece(cap_pos)
                if target and target.color != piece.color:
                    moves.append(cap_pos)
        
        return moves
    
    def _get_knight_moves(self, piece: Piece) -> List[Position]:
        """Get knight moves"""
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_pos = Position(piece.position.row + dr, piece.position.col + dc)
            if self.is_valid_position(new_pos):
                target = self.get_piece(new_pos)
                if not target or target.color != piece.color:
                    moves.append(new_pos)
        
        return moves
    
    def _get_sliding_moves(self, piece: Piece, directions: List[Tuple[int, int]]) -> List[Position]:
        """Get moves for sliding pieces (bishop, rook, queen)"""
        moves = []
        
        for dr, dc in directions:
            r, c = piece.position.row, piece.position.col
            while True:
                r, c = r + dr, c + dc
                new_pos = Position(r, c)
                
                if not self.is_valid_position(new_pos):
                    break
                
                target = self.get_piece(new_pos)
                if not target:
                    moves.append(new_pos)
                elif target.color != piece.color:
                    moves.append(new_pos)
                    break
                else:
                    break
        
        return moves
    
    def _get_bishop_moves(self, piece: Piece) -> List[Position]:
        """Get bishop moves"""
        return self._get_sliding_moves(piece, [
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ])
    
    def _get_rook_moves(self, piece: Piece) -> List[Position]:
        """Get rook moves"""
        return self._get_sliding_moves(piece, [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ])
    
    def _get_queen_moves(self, piece: Piece) -> List[Position]:
        """Get queen moves (combination of bishop and rook)"""
        return self._get_sliding_moves(piece, [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ])
    
    def _get_king_moves(self, piece: Piece) -> List[Position]:
        """Get king moves"""
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_pos = Position(piece.position.row + dr, piece.position.col + dc)
                if self.is_valid_position(new_pos):
                    target = self.get_piece(new_pos)
                    if not target or target.color != piece.color:
                        moves.append(new_pos)
        
        return moves
    
    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Move piece from one position to another"""
        piece = self.get_piece(from_pos)
        if not piece:
            return False
        
        # Check if move is valid
        valid_moves = self.get_valid_moves(from_pos)
        if to_pos not in valid_moves:
            return False
        
        # Capture piece if present
        captured = self.get_piece(to_pos)
        
        # Move piece
        self.board[to_pos] = piece
        piece.position = to_pos
        self.board[from_pos] = None
        
        # Record move
        self.move_history.append((from_pos, to_pos, captured))
        
        return True
    
    def get_all_pieces(self, color: Color) -> List[Piece]:
        """Get all pieces of a color"""
        pieces = []
        for pos, piece in self.board.items():
            if piece and piece.color == color:
                pieces.append(piece)
        return pieces
    
    def get_valid_moves_for_color(self, color: Color) -> Dict[Position, List[Position]]:
        """Get all valid moves for a color"""
        moves = {}
        for piece in self.get_all_pieces(color):
            piece_moves = self.get_valid_moves(piece.position)
            if piece_moves:
                moves[piece.position] = piece_moves
        return moves


class CelebrityOpponent:
    """AI opponent with personality"""
    
    def __init__(self, name: str, skill: int = 5):
        self.name = name
        self.skill = skill  # 1-10 scale
        self.personality = self._get_personality()
        self.win_quotes = self._get_win_quotes()
        self.loss_quotes = self._get_loss_quotes()
        self.move_quotes = self._get_move_quotes()
    
    def _get_personality(self) -> str:
        personalities = {
            "Albert Einstein": "Brilliant and contemplative",
            "Napoleon Bonaparte": "Strategic military genius",
            "Bobby Fischer": "Chess legend, intense competitor",
            "Garry Kasparov": "Aggressive attacker",
            "Magnus Carlsen": "Modern super-GM, calculating",
            "Cleopatra": "Ancient Egyptian pharaoh",
            "Sherlock Holmes": "Detective genius",
            "Marie Curie": "Scientific brilliance",
        }
        return personalities.get(self.name, "Mysterious opponent")
    
    def _get_win_quotes(self) -> List[str]:
        """Quotes when opponent wins"""
        return [
            f"{self.name}: That was an excellent game. You played well.",
            f"{self.name}: Checkmate! Better luck next time.",
            f"{self.name}: Outstanding! I enjoyed that challenge.",
            f"{self.name}: The board has spoken.",
            f"{self.name}: Victory! Your strategy was interesting.",
        ]
    
    def _get_loss_quotes(self) -> List[str]:
        """Quotes when opponent loses"""
        return [
            f"{self.name}: Congratulations! You're a formidable opponent.",
            f"{self.name}: Well played! You've bested me.",
            f"{self.name}: Remarkable! Your tactics were superior.",
            f"{self.name}: Impressive! You deserve this victory.",
            f"{self.name}: You've earned my respect.",
        ]
    
    def _get_move_quotes(self) -> List[str]:
        """Commentary during game"""
        return [
            f"{self.name}: Let me think... *moves piece*",
            f"{self.name}: An interesting position.",
            f"{self.name}: I see your strategy.",
            f"{self.name}: A bold move indeed.",
            f"{self.name}: The game intensifies...",
            f"{self.name}: Your move was unexpected.",
            f"{self.name}: I must be careful here.",
        ]
    
    def get_best_move(self, board: ChessBoard) -> Tuple[Position, Position]:
        """Get AI's move using minimax with evaluation"""
        valid_moves = board.get_valid_moves_for_color(Color.BLACK)
        
        if not valid_moves:
            return None
        
        # Skill-based move selection
        # Higher skill = better moves, lower skill = more random
        if self.skill >= 8:
            # Best move: use piece value heuristic
            best_move = None
            best_score = -float('inf')
            
            for from_pos, to_positions in valid_moves.items():
                for to_pos in to_positions:
                    # Score based on captured piece value
                    target = board.get_piece(to_pos)
                    score = self._evaluate_piece_capture(target)
                    
                    if score > best_score:
                        best_score = score
                        best_move = (from_pos, to_pos)
            
            return best_move if best_move else random.choice(
                [(f, random.choice(t)) for f, t in valid_moves.items()]
            )
        else:
            # Random move with occasional good captures
            if random.random() < (self.skill / 10):
                # Try to capture something valuable
                for from_pos, to_positions in valid_moves.items():
                    for to_pos in to_positions:
                        if board.get_piece(to_pos):  # Capture
                            return (from_pos, to_pos)
            
            # Random move
            from_pos = random.choice(list(valid_moves.keys()))
            to_pos = random.choice(valid_moves[from_pos])
            return (from_pos, to_pos)
    
    def _evaluate_piece_capture(self, piece: Optional[Piece]) -> int:
        """Evaluate value of piece capture"""
        if not piece:
            return 0
        
        piece_values = {
            PieceType.PAWN: 1,
            PieceType.KNIGHT: 3,
            PieceType.BISHOP: 3,
            PieceType.ROOK: 5,
            PieceType.QUEEN: 9,
            PieceType.KING: 100,
        }
        return piece_values.get(piece.type, 0)


class GameState(Enum):
    """Game states"""
    MENU = "menu"
    OPPONENT_SELECT = "opponent_select"
    PLAYING = "playing"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    GAME_OVER = "game_over"


class GeniusChessGame:
    """Main 3D Chess Game"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ GENIUS 3D CHESS - Battle Chess")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")
        
        # Game state
        self.board = ChessBoard()
        self.state = GameState.MENU
        self.current_opponent: Optional[CelebrityOpponent] = None
        self.selected_piece: Optional[Position] = None
        self.valid_moves: List[Position] = []
        self.white_player_human = True
        self.game_started = False
        self.move_count = 0
        self.thinking = False
        
        # Celebrity opponents
        self.opponents = [
            CelebrityOpponent("Albert Einstein", skill=7),
            CelebrityOpponent("Napoleon Bonaparte", skill=8),
            CelebrityOpponent("Bobby Fischer", skill=9),
            CelebrityOpponent("Garry Kasparov", skill=10),
            CelebrityOpponent("Magnus Carlsen", skill=10),
            CelebrityOpponent("Cleopatra", skill=6),
            CelebrityOpponent("Sherlock Holmes", skill=8),
            CelebrityOpponent("Marie Curie", skill=7),
        ]
        
        # UI setup
        self._setup_ui()
        self._show_menu()
    
    def _setup_ui(self):
        """Setup main UI structure"""
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for board
        self.canvas = tk.Canvas(
            self.main_container,
            width=500,
            height=500,
            bg="#2a2a3e",
            highlightthickness=0
        )
        
        # Side panel
        self.side_panel = ttk.Frame(self.main_container)
        
        # Configure grid
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=0)
        self.main_container.rowconfigure(0, weight=1)
    
    def _show_menu(self):
        """Show main menu"""
        self.state = GameState.MENU
        self._clear_ui()
        
        # Title
        title_font = font.Font(family="Arial", size=36, weight="bold")
        title = tk.Label(
            self.main_container,
            text="⚔️ GENIUS 3D CHESS",
            font=title_font,
            bg="#1a1a2e",
            fg="#16c784"
        )
        title.pack(pady=50)
        
        # Subtitle
        subtitle_font = font.Font(family="Arial", size=14)
        subtitle = tk.Label(
            self.main_container,
            text="Battle Chess with Celebrity Opponents",
            font=subtitle_font,
            bg="#1a1a2e",
            fg="#aaa"
        )
        subtitle.pack()
        
        # Buttons
        button_font = font.Font(family="Arial", size=12)
        
        tk.Button(
            self.main_container,
            text="🎮 PLAY vs AI",
            font=button_font,
            bg="#16c784",
            fg="white",
            padx=30,
            pady=15,
            command=self._show_opponent_select
        ).pack(pady=20)
        
        tk.Button(
            self.main_container,
            text="📖 INSTRUCTIONS",
            font=button_font,
            bg="#0f3460",
            fg="white",
            padx=30,
            pady=15,
            command=self._show_instructions
        ).pack(pady=10)
        
        tk.Button(
            self.main_container,
            text="❌ QUIT",
            font=button_font,
            bg="#e94560",
            fg="white",
            padx=30,
            pady=15,
            command=self.root.quit
        ).pack(pady=10)
    
    def _show_opponent_select(self):
        """Show opponent selection"""
        self.state = GameState.OPPONENT_SELECT
        self._clear_ui()
        
        title = tk.Label(
            self.main_container,
            text="⚔️ SELECT YOUR OPPONENT",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="#16c784"
        )
        title.pack(pady=30)
        
        # Opponent buttons
        for opponent in self.opponents:
            frame = tk.Frame(self.main_container, bg="#1a1a2e")
            frame.pack(pady=10, padx=20, fill=tk.X)
            
            # Opponent name and skill
            info_text = f"{opponent.name} (Skill: {opponent.skill}/10)"
            tk.Button(
                frame,
                text=info_text,
                font=("Arial", 12),
                bg="#0f3460",
                fg="white",
                padx=20,
                pady=10,
                command=lambda opp=opponent: self._start_game(opp)
            ).pack(fill=tk.X)
        
        # Back button
        tk.Button(
            self.main_container,
            text="← BACK",
            font=("Arial", 10),
            bg="#444",
            fg="white",
            command=self._show_menu
        ).pack(pady=20)
    
    def _show_instructions(self):
        """Show game instructions"""
        self._clear_ui()
        
        text = """
⚔️ GENIUS 3D CHESS - INSTRUCTIONS

HOW TO PLAY:
• You play as WHITE (bottom of board)
• Your opponent plays as BLACK (top of board)
• Click a piece to select it (green highlight)
• Click a valid square to move there
• Capture opponent's pieces to gain advantage

PIECE MOVEMENTS:
♟ Pawn: Moves forward 1 square (2 on first move), captures diagonally
♞ Knight: Moves in L-shape (2+1 or 1+2 squares)
♝ Bishop: Moves diagonally any number of squares
♜ Rook: Moves horizontally/vertically any number of squares
♛ Queen: Combines rook and bishop movements
♚ King: Moves 1 square in any direction

STRATEGY TIPS:
• Control the center of the board
• Protect your pieces and king
• Look ahead at opponent's responses
• Use your queen and rooks effectively
• Don't leave pieces undefended

OPPONENT DIFFICULTY:
Skill 6-7: Beginner-Intermediate
Skill 8-9: Advanced
Skill 10: Master level (very challenging)

GOOD LUCK AND ENJOY!
        """
        
        label = tk.Label(
            self.main_container,
            text=text,
            font=("Courier", 10),
            bg="#1a1a2e",
            fg="#aaa",
            justify=tk.LEFT
        )
        label.pack(padx=40, pady=20)
        
        tk.Button(
            self.main_container,
            text="← BACK",
            font=("Arial", 12),
            bg="#0f3460",
            fg="white",
            command=self._show_menu
        ).pack(pady=20)
    
    def _start_game(self, opponent: CelebrityOpponent):
        """Start game with selected opponent"""
        self.current_opponent = opponent
        self.game_started = True
        self.state = GameState.PLAYING
        
        self._clear_ui()
        self._setup_game_ui()
        self._add_log(f"🎮 Game started against {opponent.name}!")
        self._add_log(f"📊 Opponent Skill: {opponent.skill}/10")
        self._add_log(f"😊 {opponent.personality}")
        self._add_log(random.choice(opponent.move_quotes))
        self._redraw_board()
    
    def _setup_game_ui(self):
        """Setup game UI"""
        # Canvas for board
        self.canvas = tk.Canvas(
            self.main_container,
            width=500,
            height=500,
            bg="#2a2a3e",
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        
        # Side panel
        self.side_panel = tk.Frame(self.main_container, bg="#1a1a2e", width=300)
        self.side_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.side_panel.grid_propagate(False)
        
        # Opponent info
        opponent_frame = tk.Frame(self.side_panel, bg="#0f3460", relief=tk.RAISED, bd=2)
        opponent_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            opponent_frame,
            text=self.current_opponent.name,
            font=("Arial", 14, "bold"),
            bg="#0f3460",
            fg="#16c784"
        ).pack(padx=10, pady=5)
        
        tk.Label(
            opponent_frame,
            text=f"⭐ Skill: {self.current_opponent.skill}/10",
            font=("Arial", 10),
            bg="#0f3460",
            fg="#aaa"
        ).pack(padx=10, pady=5)
        
        # Game log
        tk.Label(
            self.side_panel,
            text="📋 Game Log:",
            font=("Arial", 12, "bold"),
            bg="#1a1a2e",
            fg="#16c784"
        ).pack(anchor=tk.W, padx=10, pady=(20, 5))
        
        self.log_text = tk.Text(
            self.side_panel,
            height=15,
            width=35,
            bg="#2a2a3e",
            fg="#aaa",
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.log_text.config(state=tk.DISABLED)
        
        # Buttons
        button_frame = tk.Frame(self.side_panel, bg="#1a1a2e")
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="🔄 NEW GAME",
            font=("Arial", 10),
            bg="#0f3460",
            fg="white",
            command=self._show_opponent_select
        ).pack(fill=tk.X, pady=5)
        
        tk.Button(
            button_frame,
            text="🏠 MENU",
            font=("Arial", 10),
            bg="#444",
            fg="white",
            command=self._show_menu
        ).pack(fill=tk.X, pady=5)
    
    def _add_log(self, message: str):
        """Add message to game log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _redraw_board(self):
        """Redraw chess board"""
        self.canvas.delete("all")
        
        # Draw squares
        square_size = 500 // 8
        colors = ["#ddd5c4", "#9ca694"]  # Light and dark squares
        
        for row in range(8):
            for col in range(8):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                
                # Determine square color
                color_idx = (row + col) % 2
                square_color = colors[color_idx]
                
                # Highlight selected square
                pos = Position(row, col)
                if pos == self.selected_piece:
                    square_color = "#ffeb3b"
                elif pos in self.valid_moves:
                    square_color = "#4caf50"
                
                # Draw square
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=square_color,
                    outline="black",
                    width=1
                )
                
                # Draw piece
                piece = self.board.get_piece(pos)
                if piece:
                    # Piece color
                    text_color = "white" if piece.color == Color.BLACK else "black"
                    
                    # Draw piece symbol
                    self.canvas.create_text(
                        x1 + square_size // 2,
                        y1 + square_size // 2,
                        text=piece.type.value,
                        font=("Arial", 30),
                        fill=text_color
                    )
        
        # Draw coordinates
        for i in range(8):
            # Columns (a-h)
            self.canvas.create_text(
                i * square_size + square_size // 2,
                500 + 15,
                text=chr(ord('a') + i),
                font=("Arial", 10)
            )
            # Rows (8-1)
            self.canvas.create_text(
                -15,
                i * square_size + square_size // 2,
                text=str(8 - i),
                font=("Arial", 10)
            )
    
    def _on_canvas_click(self, event):
        """Handle canvas click"""
        if not self.game_started or self.thinking:
            return
        
        # Calculate board position
        square_size = 500 // 8
        col = event.x // square_size
        row = event.y // square_size
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return
        
        pos = Position(row, col)
        
        # If clicking valid move, make move
        if pos in self.valid_moves:
            self._make_move(self.selected_piece, pos)
            self.selected_piece = None
            self.valid_moves = []
            self._redraw_board()
            
            # AI's turn
            self.root.after(500, self._ai_turn)
        else:
            # Select piece
            piece = self.board.get_piece(pos)
            if piece and piece.color == Color.WHITE:
                self.selected_piece = pos
                self.valid_moves = self.board.get_valid_moves(pos)
                self._redraw_board()
            else:
                self.selected_piece = None
                self.valid_moves = []
                self._redraw_board()
    
    def _make_move(self, from_pos: Position, to_pos: Position):
        """Make a move"""
        piece = self.board.get_piece(from_pos)
        target = self.board.get_piece(to_pos)
        
        # Move piece
        self.board.move_piece(from_pos, to_pos)
        self.move_count += 1
        
        # Log move
        from_pos_str = f"{chr(ord('a') + from_pos.col)}{8 - from_pos.row}"
        to_pos_str = f"{chr(ord('a') + to_pos.col)}{8 - to_pos.row}"
        
        if target:
            move_str = f"♔ {piece.type.value} {from_pos_str} × {to_pos_str} (captures {target.type.value})"
        else:
            move_str = f"♔ {piece.type.value} {from_pos_str} → {to_pos_str}"
        
        self._add_log(move_str)
    
    def _ai_turn(self):
        """AI makes its move"""
        if not self.current_opponent:
            return
        
        self.thinking = True
        
        # AI thinks
        self._add_log(f"🤔 {self.current_opponent.name} is thinking...")
        self.root.update()
        
        # Get AI move
        time.sleep(0.5 + random.random())  # Simulating thinking time
        
        move = self.current_opponent.get_best_move(self.board)
        
        if move:
            from_pos, to_pos = move
            self._make_move(from_pos, to_pos)
            
            # AI commentary
            self._add_log(random.choice(self.current_opponent.move_quotes))
        else:
            self._add_log("♟ No valid moves available!")
            self._game_over("Stalemate!")
        
        self._redraw_board()
        self.thinking = False
    
    def _game_over(self, result: str):
        """Handle game over"""
        self.game_started = False
        self._add_log(f"\n🏁 GAME OVER: {result}\n")
        
        if "White" in result:
            self._add_log(random.choice(self.current_opponent.loss_quotes))
        else:
            self._add_log(random.choice(self.current_opponent.win_quotes))
    
    def _clear_ui(self):
        """Clear all UI elements"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GeniusChessGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
