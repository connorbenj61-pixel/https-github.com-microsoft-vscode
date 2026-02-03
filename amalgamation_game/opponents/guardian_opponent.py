"""
ROYAL GUARDIAN OPPONENT
Royal Guard Squad Commander as competitive opponent

Implements squad-based tactical combat with four-guard formations
and skill-based advancement system.
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum
import random

from game_systems.game_engine import OpponentAI, GameState, Difficulty
from armourbound_guardian import ArmourboundGuardianAI


class GuardianFormation(Enum):
    """Squad tactical formations"""
    DIAMOND = "diamond"  # 1-2-1 balanced
    PHALANX = "phalanx"  # 1-1-1-1 defensive
    SPEAR = "spear"      # 3-1 offensive
    SHIELD = "shield"    # 1-3 defensive


class GuardRole(Enum):
    """Individual guard roles"""
    SENTINEL = "sentinel"    # Fast, agile
    PROTECTOR = "protector"  # Balanced
    WARDEN = "warden"        # Strong defense
    PALADIN = "paladin"      # High damage


@dataclass
class GuardUnit:
    """Individual guard fighter"""
    role: GuardRole
    level: int
    health: int
    attack: int
    defense: int
    experience: int
    skills: List[str]
    
    def take_damage(self, damage: int) -> None:
        """Apply damage to guard"""
        self.health = max(0, self.health - damage)
    
    def deal_damage(self) -> int:
        """Calculate damage output"""
        return self.attack + random.randint(-5, 5)


class RoyalGuardianOpponent(OpponentAI):
    """
    Royal Guardian Commander opponent
    Manages squad of 4 specialized guards with tactical formations
    """
    
    def __init__(self):
        super().__init__(
            opponent_id="guardian_commander",
            opponent_name="Royal Guardian Commander",
            base_difficulty=Difficulty.ADEPT
        )
        
        self.squad: Dict[GuardRole, GuardUnit] = {
            GuardRole.SENTINEL: GuardUnit(
                role=GuardRole.SENTINEL,
                level=1,
                health=60,
                attack=12,
                defense=8,
                experience=0,
                skills=['swift_strike', 'evasion']
            ),
            GuardRole.PROTECTOR: GuardUnit(
                role=GuardRole.PROTECTOR,
                level=1,
                health=80,
                attack=10,
                defense=10,
                experience=0,
                skills=['shield_bash', 'block']
            ),
            GuardRole.WARDEN: GuardUnit(
                role=GuardRole.WARDEN,
                level=1,
                health=100,
                attack=8,
                defense=12,
                experience=0,
                skills=['fortify', 'counter_attack']
            ),
            GuardRole.PALADIN: GuardUnit(
                role=GuardRole.PALADIN,
                level=1,
                health=90,
                attack=14,
                defense=9,
                experience=0,
                skills=['divine_strike', 'cleave']
            )
        }
        
        self.current_formation = GuardianFormation.DIAMOND
        self.mission_count = 0
        self.squad_morale = 80  # 0-100
        # Strategic planner (conceptual) — integrates external AI planner
        self.strategic_planner = ArmourboundGuardianAI()

    def get_strategic_plan(self) -> List[str]:
        """Return a high-level strategic plan from the planner.

        This is a conceptual integration used for flavor text or
        high-level decision-making, not real-time control.
        """
        return self.strategic_planner.plan_moon_mission()
    
    def prepare_for_game(self, difficulty: Difficulty) -> None:
        """Prepare guardian squad for match"""
        super().prepare_for_game(difficulty)
        
        # Scale guard stats by difficulty
        difficulty_scaling = {
            Difficulty.NOVICE: 0.7,
            Difficulty.ADEPT: 1.0,
            Difficulty.MASTER: 1.3,
            Difficulty.LEGENDARY: 1.6,
            Difficulty.AMALGAMATED: 2.0
        }
        
        scale = difficulty_scaling.get(difficulty, 1.0)
        
        for guard in self.squad.values():
            guard.health = int(guard.health * scale)
            guard.attack = int(guard.attack * scale)
            guard.defense = int(guard.defense * scale)
            guard.level = int(difficulty.value * 2)
    
    def compute_move(self, game_state: GameState, 
                     player_move: Dict) -> Dict:
        """
        Compute guardian squad tactical response
        Analyzes player threat and coordinates squad action
        """
        super().compute_move(game_state, player_move)
        
        # Step 1: Assess threat
        threat_assessment = self._assess_threat(player_move)
        
        # Step 2: Select formation
        optimal_formation = self._select_formation(threat_assessment)
        self.current_formation = optimal_formation
        
        # Step 3: Assign guards
        formation_assignment = self._assign_guards_to_formation()
        
        # Step 4: Coordinate attack
        coordinated_action = self._coordinate_squad_action(
            formation_assignment,
            threat_assessment
        )
        
        return {
            'type': 'squad_tactical_action',
            'formation': self.current_formation.value,
            'action': coordinated_action,
            'squad_morale': self.squad_morale,
            'confidence': min(1.0, self.squad_morale / 100),
            'rationale': f"Guardian squad executes {optimal_formation.value} formation"
        }
    
    def _assess_threat(self, player_move: Dict) -> Dict:
        """Analyze player move for threat level"""
        threat_level = 5  # 1-10 scale
        
        if player_move.get('aggression', 0) > 0.7:
            threat_level = 8
        elif player_move.get('defense', 0) > 0.7:
            threat_level = 3
        elif player_move.get('special', False):
            threat_level = 7
        
        return {
            'threat_level': threat_level,
            'target_role': random.choice(list(GuardRole)),
            'estimated_damage': threat_level * random.randint(5, 15)
        }
    
    def _select_formation(self, threat: Dict) -> GuardianFormation:
        """Select optimal formation based on threat assessment"""
        threat_level = threat['threat_level']
        
        if threat_level >= 8:
            return GuardianFormation.SHIELD  # Defensive
        elif threat_level >= 6:
            return GuardianFormation.DIAMOND  # Balanced
        elif threat_level >= 4:
            return GuardianFormation.PHALANX  # Flexible defense
        else:
            return GuardianFormation.SPEAR    # Offensive
    
    def _assign_guards_to_formation(self) -> Dict[str, GuardRole]:
        """Assign guards to formation positions"""
        if self.current_formation == GuardianFormation.DIAMOND:
            return {
                'front': GuardRole.PROTECTOR,
                'flanks': [GuardRole.SENTINEL, GuardRole.SENTINEL],
                'rear': GuardRole.PALADIN,
                'reserve': GuardRole.WARDEN
            }
        elif self.current_formation == GuardianFormation.SHIELD:
            return {
                'front': GuardRole.WARDEN,
                'flanks': [GuardRole.WARDEN, GuardRole.PROTECTOR],
                'rear': GuardRole.PALADIN,
                'reserve': GuardRole.SENTINEL
            }
        elif self.current_formation == GuardianFormation.PHALANX:
            return {
                'front': GuardRole.SENTINEL,
                'flanks': [GuardRole.PROTECTOR, GuardRole.WARDEN],
                'rear': GuardRole.PALADIN,
                'reserve': GuardRole.SENTINEL
            }
        else:  # SPEAR
            return {
                'front': GuardRole.PALADIN,
                'flanks': [GuardRole.SENTINEL, GuardRole.SENTINEL],
                'rear': GuardRole.PROTECTOR,
                'reserve': GuardRole.WARDEN
            }
    
    def _coordinate_squad_action(self, formation: Dict, 
                                threat: Dict) -> Dict:
        """Coordinate unified squad action"""
        primary_attacker = formation['front']
        guard = self.squad[primary_attacker]
        
        damage = guard.deal_damage()
        
        # Morale affects coordination
        morale_bonus = 1 + (self.squad_morale - 80) / 100
        adjusted_damage = int(damage * morale_bonus)
        
        return {
            'primary_attacker': primary_attacker.value,
            'damage': adjusted_damage,
            'formation': self.current_formation.value,
            'coordination_level': morale_bonus
        }
    
    def train_squad(self) -> None:
        """Improve squad through training"""
        for guard in self.squad.values():
            guard.level += 1
            guard.experience += 50
            guard.health += 5
            guard.attack += 2
            guard.defense += 1
        
        self.squad_morale = min(100, self.squad_morale + 5)
        self.mission_count += 1
    
    def rest_squad(self) -> None:
        """Restore squad health and morale"""
        for guard in self.squad.values():
            guard.health = int(guard.health * 1.1)
        
        self.squad_morale = min(100, self.squad_morale + 10)
