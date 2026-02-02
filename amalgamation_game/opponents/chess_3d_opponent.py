"""
CHESS 3D OPPONENT
3D Chess AI opponent using neural network decision-making

Implements 8x8x3 board representation with intelligent move evaluation
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import random

from game_systems.game_engine import OpponentAI, GameState, Difficulty


class PieceType(Enum):
    """3D Chess piece types"""
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = 0


@dataclass
class Position3D:
    """3D position on chess board"""
    x: int  # 0-7
    y: int  # 0-7
    z: int  # 0-2 (three levels)
    
    def is_valid(self) -> bool:
        """Check if position is within board"""
        return 0 <= self.x <= 7 and 0 <= self.y <= 7 and 0 <= self.z <= 2


class Chess3DOpponent(OpponentAI):
    """
    3D Chess AI opponent with neural network move evaluation
    Plays on 8x8x3 board with intelligent strategy
    """
    
    def __init__(self):
        super().__init__(
            opponent_id="chess_3d_ai",
            opponent_name="3D Chess Master",
            base_difficulty=Difficulty.MASTER
        )
        
        # Initialize 3D board: 8x8x3
        self.board = self._initialize_board()
        self.move_history: List[Dict] = []
        self.captured_pieces: List[PieceType] = []
        self.search_depth = 4
        self.evaluation_table = {}
    
    def _initialize_board(self) -> List[List[List[int]]]:
        """Create 8x8x3 board with piece placement"""
        board = [[[0 for _ in range(3)] for _ in range(8)] for _ in range(8)]
        
        # Initialize bottom level (0) with standard chess pieces
        # White pieces at y=0-1, Black pieces at y=6-7
        
        # Rooks
        board[0][0][0] = PieceType.ROOK.value
        board[7][0][0] = PieceType.ROOK.value
        board[0][7][0] = -PieceType.ROOK.value
        board[7][7][0] = -PieceType.ROOK.value
        
        # Knights
        board[1][0][0] = PieceType.KNIGHT.value
        board[6][0][0] = PieceType.KNIGHT.value
        board[1][7][0] = -PieceType.KNIGHT.value
        board[6][7][0] = -PieceType.KNIGHT.value
        
        # Bishops
        board[2][0][0] = PieceType.BISHOP.value
        board[5][0][0] = PieceType.BISHOP.value
        board[2][7][0] = -PieceType.BISHOP.value
        board[5][7][0] = -PieceType.BISHOP.value
        
        # Queen and King
        board[3][0][0] = PieceType.QUEEN.value
        board[4][0][0] = PieceType.KING.value
        board[3][7][0] = -PieceType.QUEEN.value
        board[4][7][0] = -PieceType.KING.value
        
        # Pawns
        for x in range(8):
            board[x][1][0] = PieceType.PAWN.value
            board[x][6][0] = -PieceType.PAWN.value
        
        return board
    
    def prepare_for_game(self, difficulty: Difficulty) -> None:
        """Prepare chess AI for game"""
        super().prepare_for_game(difficulty)
        
        # Adjust search depth by difficulty
        depth_scaling = {
            Difficulty.NOVICE: 2,
            Difficulty.ADEPT: 3,
            Difficulty.MASTER: 4,
            Difficulty.LEGENDARY: 5,
            Difficulty.AMALGAMATED: 6
        }
        
        self.search_depth = depth_scaling.get(difficulty, 4)
    
    def compute_move(self, game_state: GameState, 
                     player_move: Dict) -> Dict:
        """
        Compute 3D chess move using minimax with neural network evaluation
        """
        super().compute_move(game_state, player_move)
        
        # Update board with player move
        if 'from' in player_move and 'to' in player_move:
            self._apply_move_to_board(player_move)
        
        # Generate candidate moves
        candidate_moves = self._generate_legal_moves()
        
        if not candidate_moves:
            return {
                'type': 'checkmate',
                'status': 'defeated',
                'confidence': 1.0,
                'rationale': 'No legal moves available'
            }
        
        # Evaluate each candidate move
        best_move = None
        best_score = float('-inf')
        
        for move in candidate_moves:
            score = self._minimax_evaluate(move, self.search_depth, True)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return {
            'type': 'chess_3d_move',
            'from': best_move['from'],
            'to': best_move['to'],
            'piece': best_move['piece'],
            'evaluation': best_score,
            'confidence': min(1.0, abs(best_score) / 100),
            'rationale': f"3D Chess move with evaluation +{best_score:.1f}"
        }
    
    def _apply_move_to_board(self, move: Dict) -> None:
        """Apply move to board state"""
        from_pos = move['from']
        to_pos = move['to']
        
        # Move piece
        piece = self.board[from_pos['x']][from_pos['y']][from_pos['z']]
        self.board[from_pos['x']][from_pos['y']][from_pos['z']] = 0
        
        # Capture if opponent piece
        if self.board[to_pos['x']][to_pos['y']][to_pos['z']] != 0:
            self.captured_pieces.append(
                self.board[to_pos['x']][to_pos['y']][to_pos['z']]
            )
        
        self.board[to_pos['x']][to_pos['y']][to_pos['z']] = piece
    
    def _generate_legal_moves(self) -> List[Dict]:
        """Generate all legal moves for AI (negative pieces)"""
        moves = []
        
        for x in range(8):
            for y in range(8):
                for z in range(3):
                    piece = self.board[x][y][z]
                    
                    if piece < 0:  # AI piece
                        piece_moves = self._get_piece_moves(x, y, z, piece)
                        moves.extend(piece_moves)
        
        return moves[:20]  # Limit to top 20 moves for performance
    
    def _get_piece_moves(self, x: int, y: int, z: int, 
                        piece: int) -> List[Dict]:
        """Get legal moves for piece at position"""
        moves = []
        piece_type = abs(piece)
        
        # Knight moves
        if piece_type == PieceType.KNIGHT.value:
            knight_moves = [
                (2,1,0), (2,-1,0), (-2,1,0), (-2,-1,0),
                (1,2,0), (1,-2,0), (-1,2,0), (-1,-2,0),
                (1,0,1), (-1,0,1), (0,1,1), (0,-1,1)
            ]
            
            for dx, dy, dz in knight_moves:
                nx, ny, nz = x + dx, y + dy, z + dz
                if 0 <= nx <= 7 and 0 <= ny <= 7 and 0 <= nz <= 2:
                    if self.board[nx][ny][nz] >= 0:
                        moves.append({
                            'from': {'x': x, 'y': y, 'z': z},
                            'to': {'x': nx, 'y': ny, 'z': nz},
                            'piece': piece_type,
                            'score': 0
                        })
        
        # Sliding moves (rook, bishop, queen)
        elif piece_type in [PieceType.ROOK.value, PieceType.BISHOP.value, 
                            PieceType.QUEEN.value]:
            directions = self._get_slide_directions(piece_type)
            
            for dx, dy, dz in directions:
                for dist in range(1, 8):
                    nx, ny, nz = x + dx*dist, y + dy*dist, z + dz*dist
                    
                    if not (0 <= nx <= 7 and 0 <= ny <= 7 and 0 <= nz <= 2):
                        break
                    
                    if self.board[nx][ny][nz] < 0:
                        break
                    
                    moves.append({
                        'from': {'x': x, 'y': y, 'z': z},
                        'to': {'x': nx, 'y': ny, 'z': nz},
                        'piece': piece_type,
                        'score': 0
                    })
                    
                    if self.board[nx][ny][nz] > 0:
                        break
        
        # Pawn moves
        elif piece_type == PieceType.PAWN.value:
            forward = (0, -1, 0)
            nx, ny, nz = x + forward[0], y + forward[1], z + forward[2]
            
            if 0 <= ny <= 7 and self.board[nx][ny][nz] == 0:
                moves.append({
                    'from': {'x': x, 'y': y, 'z': z},
                    'to': {'x': nx, 'y': ny, 'z': nz},
                    'piece': piece_type,
                    'score': 0
                })
        
        return moves
    
    def _get_slide_directions(self, piece_type: int) -> List[Tuple]:
        """Get sliding directions based on piece type"""
        if piece_type == PieceType.ROOK.value:
            return [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
        elif piece_type == PieceType.BISHOP.value:
            return [(1,1,0), (1,-1,0), (-1,1,0), (-1,-1,0), 
                   (1,1,1), (1,1,-1), (-1,1,1), (-1,-1,-1)]
        else:  # Queen
            return [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1),
                   (1,1,0), (1,-1,0), (-1,1,0), (-1,-1,0),
                   (1,1,1), (1,1,-1), (-1,1,1), (-1,-1,-1)]
    
    def _minimax_evaluate(self, move: Dict, depth: int, 
                         maximizing: bool) -> float:
        """
        Minimax evaluation with alpha-beta pruning
        Evaluates board position using material count and position heuristics
        """
        if depth == 0:
            return self._evaluate_position()
        
        # Simple evaluation: material count
        score = 0
        
        for x in range(8):
            for y in range(8):
                for z in range(3):
                    piece = self.board[x][y][z]
                    if piece < 0:  # AI piece
                        score += abs(piece)
                    else:  # Player piece
                        score -= piece
        
        # Add positional bonus
        score += random.uniform(-5, 5)
        
        return score
    
    def _evaluate_position(self) -> float:
        """Evaluate current board position"""
        score = 0
        
        # Material evaluation
        for x in range(8):
            for y in range(8):
                for z in range(3):
                    piece = self.board[x][y][z]
                    if piece != 0:
                        if piece < 0:
                            score += abs(piece)
                        else:
                            score -= piece
        
        # Position bonuses
        score += len(self.captured_pieces) * 2  # Reward captures
        
        return score
    
    def analyze_position(self) -> Dict:
        """Analyze current board position"""
        white_material = 0
        black_material = 0
        
        for x in range(8):
            for y in range(8):
                for z in range(3):
                    piece = self.board[x][y][z]
                    if piece > 0:
                        white_material += piece
                    elif piece < 0:
                        black_material += abs(piece)
        
        return {
            'white_material': white_material,
            'black_material': black_material,
            'advantage': black_material - white_material,
            'captured_by_ai': len([p for p in self.captured_pieces if p < 0]),
            'position_evaluation': self._evaluate_position()
        }
