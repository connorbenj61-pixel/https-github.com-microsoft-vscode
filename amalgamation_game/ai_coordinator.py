"""
AI COORDINATOR - Multi-Agent Strategic Planning System

Integrates ArmourboundGuardianAI with game opponents and provides
coordinated AI reasoning across the Amalgamation Game ecosystem.

This module serves as the central hub for:
- Opponent AI registration and discovery
- Strategic planning coordination
- Inter-agent communication
- Mission planning and domain learning
"""

import sys
from pathlib import Path

# Add parent directory to path so armourbound_guardian can be imported
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from amalgamation_game.armourbound_guardian import ArmourboundGuardianAI
from game_systems.game_engine import Difficulty


class AICoordinator:
    """Central hub for multi-agent AI coordination in the Amalgamation Game."""
    
    def __init__(self):
        """Initialize the AI coordinator with the strategic planner."""
        self.guardian_planner = ArmourboundGuardianAI()
        self.guardian_planner.register_as("Strategic_Planner")
        self.active_opponents = {}
        self.mission_plans = {}
    
    def register_opponent(self, opponent_name: str, opponent_ai) -> None:
        """
        Register a game opponent with the coordinator.
        Enables the opponent to communicate with the strategic planner.
        
        Args:
            opponent_name: Name of the opponent AI
            opponent_ai: Instance of the opponent AI class
        """
        self.active_opponents[opponent_name] = opponent_ai
        
        # If opponent has strategic planner integration, register it
        if hasattr(opponent_ai, 'strategic_planner'):
            opponent_ai.strategic_planner.register_as(opponent_name)
    
    def generate_mission_plan(self, mission_type: str = "moon") -> list:
        """
        Generate a strategic mission plan using the planner.
        
        Args:
            mission_type: Type of mission (default: "moon")
            
        Returns:
            List of mission planning steps
        """
        plan = self.guardian_planner.plan_moon_mission()
        self.mission_plans[mission_type] = plan
        return plan
    
    def get_tactical_reasoning(self, phase: str, difficulty: Difficulty) -> str:
        """
        Get contextual reasoning for a specific mission phase.
        
        Args:
            phase: Mission phase (objectives, vehicle, trajectory, systems, risk, execute)
            difficulty: Game difficulty level (scales reasoning depth)
            
        Returns:
            Tactical reasoning guidance
        """
        reasoning = self.guardian_planner.reason_step_toward_moon({"phase": phase})
        
        # Enhance with difficulty scaling
        if difficulty == Difficulty.LEGENDARY:
            reasoning += " [Advanced tactical considerations apply at LEGENDARY difficulty]"
        elif difficulty == Difficulty.NOVICE:
            reasoning += " [Simplified approach for NOVICE level]"
        
        return reasoning
    
    def coordinate_opponent_message(self, sender_name: str, recipient_name: str, 
                                   message: str) -> dict:
        """
        Coordinate a message between game opponents or to the strategic planner.
        
        Args:
            sender_name: Name of the sending opponent
            recipient_name: Name of the recipient opponent or planner
            message: Message content
            
        Returns:
            Dictionary with response and metadata
        """
        if sender_name in self.active_opponents:
            sender = self.active_opponents[sender_name]
            
            # If recipient is the strategic planner
            if recipient_name == "Strategic_Planner":
                return self.guardian_planner.send_message(
                    "Strategic_Planner",
                    message,
                    {"sender": sender_name, "difficulty": getattr(sender, 'difficulty', None)}
                )
            
            # If both are registered opponents
            if hasattr(sender, 'send_message'):
                return sender.send_message(recipient_name, message)
        
        return {"success": False, "error": f"Sender '{sender_name}' not found"}
    
    def learn_domain(self, domain: str) -> list:
        """
        Get a learning plan for a specific domain.
        
        Args:
            domain: Domain name (dolphins, moon, ancient_runes, quantum_mechanics, etc.)
            
        Returns:
            List of learning steps for the domain
        """
        return self.guardian_planner.learn_domain_language(domain)
    
    def get_opponent_strategic_plan(self, opponent_name: str) -> list:
        """
        Retrieve strategic plan from an opponent if available.
        
        Args:
            opponent_name: Name of the opponent
            
        Returns:
            List of strategic planning steps, or empty list if not available
        """
        if opponent_name in self.active_opponents:
            opponent = self.active_opponents[opponent_name]
            if hasattr(opponent, 'get_strategic_plan'):
                return opponent.get_strategic_plan()
        
        return []
    
    def list_all_agents(self) -> dict:
        """
        List all registered AIs in the game ecosystem.
        
        Returns:
            Dictionary containing planner and active opponents
        """
        return {
            "strategic_planner": "Strategic_Planner",
            "active_opponents": list(self.active_opponents.keys()),
            "total_agents": len(self.active_opponents) + 1
        }
    
    def broadcast_mission_briefing(self) -> dict:
        """
        Generate a mission briefing for all active opponents.
        
        Returns:
            Dictionary with mission overview and plans
        """
        plan = self.generate_mission_plan("moon")
        
        briefing = {
            "mission_type": "Moon Expedition",
            "total_phases": len(plan),
            "first_phase": plan[0] if plan else "No plan available",
            "participating_opponents": list(self.active_opponents.keys()),
            "strategic_planner": "Strategic_Planner",
            "full_plan_available": True
        }
        
        return briefing


# Global coordinator instance
_global_coordinator = None


def get_coordinator() -> AICoordinator:
    """Get or create the global AI coordinator instance."""
    global _global_coordinator
    if _global_coordinator is None:
        _global_coordinator = AICoordinator()
    return _global_coordinator


def initialize_coordinator() -> AICoordinator:
    """Initialize the global AI coordinator."""
    global _global_coordinator
    _global_coordinator = AICoordinator()
    return _global_coordinator
