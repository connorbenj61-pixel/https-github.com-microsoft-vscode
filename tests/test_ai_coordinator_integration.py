"""
Integration tests for AI Coordinator with the Amalgamation Game.

Tests the coordinator's ability to:
- Initialize and manage multiple AIs
- Coordinate inter-agent communication
- Generate mission plans
- Integrate with game opponents
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from amalgamation_game.ai_coordinator import AICoordinator, initialize_coordinator, get_coordinator
from game_systems.game_engine import Difficulty


class TestAICoordinator(unittest.TestCase):
    
    def setUp(self):
        """Reset coordinator before each test."""
        from amalgamation_game import ai_coordinator
        ai_coordinator._global_coordinator = None
    
    def test_coordinator_initialization(self):
        """Test that coordinator initializes correctly."""
        coordinator = AICoordinator()
        
        self.assertIsNotNone(coordinator.guardian_planner)
        self.assertEqual(len(coordinator.active_opponents), 0)
        self.assertIsInstance(coordinator.mission_plans, dict)
    
    def test_generate_moon_mission_plan(self):
        """Test moon mission plan generation."""
        coordinator = AICoordinator()
        plan = coordinator.generate_mission_plan("moon")
        
        self.assertIsInstance(plan, list)
        self.assertGreaterEqual(len(plan), 24)
        self.assertIn("moon", coordinator.mission_plans)
    
    def test_tactical_reasoning_by_phase(self):
        """Test tactical reasoning for different mission phases."""
        coordinator = AICoordinator()
        
        phases = ["objectives", "vehicle", "trajectory", "systems", "risk", "execute"]
        for phase in phases:
            reasoning = coordinator.get_tactical_reasoning(phase, Difficulty.ADEPT)
            self.assertIsInstance(reasoning, str)
            self.assertGreater(len(reasoning), 10)
    
    def test_difficulty_scaling_in_reasoning(self):
        """Test that reasoning adapts to difficulty level."""
        coordinator = AICoordinator()
        
        novice_reasoning = coordinator.get_tactical_reasoning("objectives", Difficulty.NOVICE)
        self.assertIn("NOVICE", novice_reasoning)
        
        legendary_reasoning = coordinator.get_tactical_reasoning("objectives", Difficulty.LEGENDARY)
        self.assertIn("LEGENDARY", legendary_reasoning)
    
    def test_domain_learning_integration(self):
        """Test domain learning through coordinator."""
        coordinator = AICoordinator()
        
        # Test dolphin learning
        dolphin_plan = coordinator.learn_domain("dolphins")
        self.assertIsInstance(dolphin_plan, list)
        self.assertGreaterEqual(len(dolphin_plan), 10)
        self.assertTrue(any("dolphin" in step.lower() for step in dolphin_plan))
    
    def test_list_all_agents(self):
        """Test listing all registered agents."""
        coordinator = AICoordinator()
        agents = coordinator.list_all_agents()
        
        self.assertEqual(agents["strategic_planner"], "Strategic_Planner")
        self.assertEqual(agents["total_agents"], 1)  # Just the planner
    
    def test_mission_briefing(self):
        """Test mission briefing generation."""
        coordinator = AICoordinator()
        briefing = coordinator.broadcast_mission_briefing()
        
        self.assertEqual(briefing["mission_type"], "Moon Expedition")
        self.assertGreater(briefing["total_phases"], 0)
        self.assertTrue(briefing["full_plan_available"])
    
    def test_global_coordinator_singleton(self):
        """Test that global coordinator works as singleton."""
        coord1 = get_coordinator()
        coord2 = get_coordinator()
        
        self.assertIs(coord1, coord2)
    
    def test_initialize_coordinator(self):
        """Test coordinator initialization function."""
        initialized = initialize_coordinator()
        
        self.assertIsNotNone(initialized)
        self.assertEqual(initialized.list_all_agents()["total_agents"], 1)


if __name__ == '__main__':
    unittest.main()
