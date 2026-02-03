import unittest
from typing import List


class TestArmourboundIntegration(unittest.TestCase):
    def test_plan_moon_mission_contents(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        plan = ai.plan_moon_mission()

        self.assertIsInstance(plan, list)
        self.assertGreaterEqual(len(plan), 24)
        self.assertTrue(plan[0].lower().startswith("define mission objectives"))

    def test_guardian_get_strategic_plan(self):
        # Import the opponent which integrates the planner
        from amalgamation_game.opponents.guardian_opponent import RoyalGuardianOpponent

        opp = RoyalGuardianOpponent()
        strategy = opp.get_strategic_plan()

        self.assertIsInstance(strategy, list)
        # Ensure integration returns the same first step
        self.assertTrue(strategy[0].lower().startswith("define mission objectives"))

    def test_reason_step_toward_moon(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()

        # Test default (no context) — returns objectives phase
        reason = ai.reason_step_toward_moon()
        self.assertIsInstance(reason, str)
        self.assertIn("crewed mission", reason)

        # Test fallback case (unknown phase)
        reason = ai.reason_step_toward_moon({"phase": "unknown"})
        self.assertIn("Council Protector", reason)

        # Test each phase
        phases = ["objectives", "vehicle", "trajectory", "systems", "risk", "execute"]
        for phase in phases:
            reason = ai.reason_step_toward_moon({"phase": phase})
            self.assertIsInstance(reason, str)
            self.assertGreater(len(reason), 10)

    def test_learn_domain_language_dolphins(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        
        # Test dolphin language learning plan
        dolphin_plan = ai.learn_domain_language("dolphins")
        self.assertIsInstance(dolphin_plan, list)
        self.assertGreaterEqual(len(dolphin_plan), 10)
        self.assertTrue(any("bioacoustics" in step.lower() for step in dolphin_plan))
        self.assertTrue(any("dolphin" in step.lower() for step in dolphin_plan))

    def test_learn_domain_language_moon(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        
        # Test that 'moon' domain returns the moon mission plan
        moon_plan = ai.learn_domain_language("moon")
        mission_plan = ai.plan_moon_mission()
        self.assertEqual(moon_plan, mission_plan)

    def test_learn_domain_language_ancient_runes(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        
        # Test ancient runes learning plan
        runes_plan = ai.learn_domain_language("ancient_runes")
        self.assertIsInstance(runes_plan, list)
        self.assertGreaterEqual(len(runes_plan), 10)
        self.assertTrue(any("futhark" in step.lower() for step in runes_plan))

    def test_learn_domain_language_quantum_mechanics(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        
        # Test quantum mechanics learning plan
        quantum_plan = ai.learn_domain_language("quantum_mechanics")
        self.assertIsInstance(quantum_plan, list)
        self.assertGreaterEqual(len(quantum_plan), 10)
        self.assertTrue(any("schrödinger" in step.lower() for step in quantum_plan))

    def test_learn_domain_language_fallback(self):
        from armourbound_guardian import ArmourboundGuardianAI

        ai = ArmourboundGuardianAI()
        
        # Test generic fallback for unknown domain
        unknown_plan = ai.learn_domain_language("cryptozoology")
        self.assertIsInstance(unknown_plan, list)
        self.assertGreaterEqual(len(unknown_plan), 10)
        self.assertTrue(any("Council Protector" in step for step in unknown_plan))


if __name__ == '__main__':
    unittest.main()
