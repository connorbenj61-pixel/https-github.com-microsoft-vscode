"""
NECROMANCER OPPONENT
Royal Necromancer as AI adversary in Amalgamation Game

Implements 163-IQ strategic cognition with three guardian protocols
and alignment-based decision making.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum
import random
import time

from game_systems.game_engine import OpponentAI, GameState, Difficulty


class NecromancerStrategy(Enum):
    """Strategic archetypes for Necromancer"""
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    STRATEGIC = "strategic"
    BALANCED = "balanced"


@dataclass
class ProtocolState:
    """Guardian protocol state tracking"""
    name: str
    active: bool = True
    efficacy: float = 1.0
    alignment_bias: int = 0


class NecromancerOpponent(OpponentAI):
    """
    Royal Necromancer opponent with 163-IQ strategic cognition
    Uses three guardian protocols: CrownJeweller, XNOR Blood Code, HighMind Circuit
    """
    
    def __init__(self):
        super().__init__(
            opponent_id="necromancer_signet",
            opponent_name="Royal Necromancer",
            base_difficulty=Difficulty.MASTER
        )
        
        self.cognition_iq = 163
        self.alignment = 50  # 0-100 scale
        self.protocols = {
            'crown_jeweller': ProtocolState('CrownJeweller', True, 1.0, 0),
            'xnor_blood': ProtocolState('XNOR Blood Code', True, 1.0, 0),
            'highmind': ProtocolState('HighMind Circuit', True, 1.0, 0)
        }
        self.vow_count = 0
        self.strategy = NecromancerStrategy.BALANCED
        self.prediction_accuracy = 0.75
    
    def prepare_for_game(self, difficulty: Difficulty) -> None:
        """Prepare Necromancer for match"""
        super().prepare_for_game(difficulty)
        
        # Adjust cognition effectiveness
        cognition_boost = {
            Difficulty.NOVICE: 0.6,
            Difficulty.ADEPT: 0.8,
            Difficulty.MASTER: 1.0,
            Difficulty.LEGENDARY: 1.2,
            Difficulty.AMALGAMATED: 1.5
        }
        
        self.prediction_accuracy = 0.75 * cognition_boost.get(difficulty, 1.0)
        
        # Determine strategy for difficulty
        if difficulty == Difficulty.NOVICE:
            self.strategy = NecromancerStrategy.DEFENSIVE
        elif difficulty == Difficulty.ADEPT:
            self.strategy = NecromancerStrategy.BALANCED
        elif difficulty == Difficulty.MASTER:
            self.strategy = NecromancerStrategy.STRATEGIC
        else:
            self.strategy = NecromancerStrategy.AGGRESSIVE
    
    def compute_move(self, game_state: GameState, 
                     player_move: Dict) -> Dict:
        """
        Compute Necromancer's move using 163-IQ strategic analysis
        Integrates all three guardian protocols
        """
        super().compute_move(game_state, player_move)
        
        # Phase 1: Analyze player move with HighMind Circuit
        player_analysis = self._analyze_player_intent(player_move)
        
        # Phase 2: Apply protocol hierarchy
        protocol_response = self._invoke_protocols(player_analysis, game_state)
        
        # Phase 3: Generate strategic move
        strategic_move = self._execute_strategy(
            player_analysis,
            protocol_response,
            game_state
        )
        
        # Phase 4: Apply alignment filters
        final_move = self._apply_alignment_filter(strategic_move)
        
        return final_move
    
    def _analyze_player_intent(self, player_move: Dict) -> Dict:
        """
        HighMind Circuit: Analyze player's strategic intent
        Uses 163-IQ pattern recognition
        """
        analysis = {
            'predicted_intent': None,
            'confidence': random.uniform(0.6, 0.95),
            'threat_level': random.randint(1, 10),
            'opportunity': random.randint(1, 10),
            'patterns_detected': []
        }
        
        # High-IQ analysis
        if random.random() < self.prediction_accuracy:
            move_type = player_move.get('type', 'unknown')
            analysis['predicted_intent'] = f"Detected: {move_type}"
            analysis['patterns_detected'] = self._extract_patterns(player_move)
        
        return analysis
    
    def _extract_patterns(self, move: Dict) -> List[str]:
        """Extract strategic patterns from player move"""
        patterns = []
        
        if move.get('aggression', False):
            patterns.append('OFFENSIVE_PRESSURE')
        if move.get('defense', False):
            patterns.append('POSITION_FORTIFICATION')
        if move.get('tempo'):
            patterns.append('TEMPO_CONTROL')
        
        return patterns
    
    def _invoke_protocols(self, analysis: Dict, 
                         game_state: GameState) -> Dict:
        """
        Invoke guardian protocols in hierarchy:
        1. CrownJeweller (resource management)
        2. XNOR Blood Code (logical consistency)
        3. HighMind Circuit (strategic synthesis)
        """
        protocol_decisions = {}
        
        # CrownJeweller: Optimize resource allocation
        if self.protocols['crown_jeweller'].active:
            protocol_decisions['resources'] = self._crown_jeweller_decision(
                game_state
            )
        
        # XNOR Blood Code: Maintain logical consistency
        if self.protocols['xnor_blood'].active:
            protocol_decisions['consistency'] = self._xnor_blood_decision(
                analysis
            )
        
        # HighMind Circuit: Strategic synthesis
        if self.protocols['highmind'].active:
            protocol_decisions['synthesis'] = self._highmind_synthesis(
                analysis,
                game_state
            )
        
        return protocol_decisions
    
    def _crown_jeweller_decision(self, game_state: GameState) -> Dict:
        """CrownJeweller protocol: Resource optimization"""
        return {
            'resource_priority': 'maximize_efficiency',
            'allocation': random.uniform(0.7, 1.0),
            'protect_assets': game_state.player_score > game_state.opponent_score
        }
    
    def _xnor_blood_decision(self, analysis: Dict) -> Dict:
        """XNOR Blood Code: Logical consistency enforcement"""
        return {
            'logical_gate': 'enforce_consistency',
            'alignment_check': self.alignment > 50,
            'vow_honor': self.vow_count > 0
        }
    
    def _highmind_synthesis(self, analysis: Dict, 
                           game_state: GameState) -> Dict:
        """HighMind Circuit: Strategic synthesis"""
        threat = analysis['threat_level']
        opportunity = analysis['opportunity']
        
        return {
            'synthesis_level': 'high_cognition',
            'aggression_factor': (opportunity - threat) / 20,
            'predicted_player_elo': game_state.player_id
        }
    
    def _execute_strategy(self, analysis: Dict, protocols: Dict,
                         game_state: GameState) -> Dict:
        """Execute Necromancer's strategic move"""
        
        if self.strategy == NecromancerStrategy.AGGRESSIVE:
            return self._aggressive_strategy(analysis, protocols)
        elif self.strategy == NecromancerStrategy.DEFENSIVE:
            return self._defensive_strategy(analysis, protocols)
        elif self.strategy == NecromancerStrategy.STRATEGIC:
            return self._strategic_strategy(analysis, protocols)
        else:
            return self._balanced_strategy(analysis, protocols)
    
    def _aggressive_strategy(self, analysis: Dict, 
                            protocols: Dict) -> Dict:
        """Aggressive tactical approach"""
        return {
            'type': 'aggressive_strike',
            'intensity': random.uniform(0.8, 1.0),
            'target': 'opponent_weakness',
            'risk_level': 0.8
        }
    
    def _defensive_strategy(self, analysis: Dict, 
                           protocols: Dict) -> Dict:
        """Defensive fortification approach"""
        return {
            'type': 'defensive_fortification',
            'intensity': random.uniform(0.5, 0.7),
            'focus': 'preserve_position',
            'risk_level': 0.2
        }
    
    def _strategic_strategy(self, analysis: Dict, 
                           protocols: Dict) -> Dict:
        """Strategic long-term positioning"""
        return {
            'type': 'strategic_positioning',
            'intensity': random.uniform(0.6, 0.9),
            'horizon': 5,  # moves ahead
            'risk_level': 0.5
        }
    
    def _balanced_strategy(self, analysis: Dict, 
                          protocols: Dict) -> Dict:
        """Balanced approach adapting to situation"""
        threat = analysis.get('threat_level', 5)
        
        if threat > 7:
            return self._defensive_strategy(analysis, protocols)
        elif threat < 3:
            return self._aggressive_strategy(analysis, protocols)
        else:
            return self._strategic_strategy(analysis, protocols)
    
    def _apply_alignment_filter(self, move: Dict) -> Dict:
        """Apply alignment-based filtering to move"""
        # If highly evil-aligned, more aggressive
        # If good-aligned, more defensive
        
        aggression_mod = (self.alignment - 50) / 100
        
        move['alignment_adjusted'] = True
        move['alignment_bias'] = self.alignment
        move['confidence'] = move.get('confidence', 0.5) + (aggression_mod * 0.1)
        move['rationale'] = (
            f"Necromancer executes {move.get('type', 'move')} "
            f"with {int(move['confidence']*100)}% confidence"
        )
        
        return move
    
    def record_victory(self) -> None:
        """Update Necromancer state after victory"""
        self.alignment = min(100, self.alignment + 2)
        self.vow_count += 1
    
    def record_defeat(self) -> None:
        """Update Necromancer state after defeat"""
        self.alignment = max(0, self.alignment - 2)
        self.vow_count = max(0, self.vow_count - 1)
