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


if __name__ == '__main__':
    unittest.main()
