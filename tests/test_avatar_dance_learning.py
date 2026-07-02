import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import avatar_dance_learning


class AvatarDanceLearningTests(unittest.TestCase):
    def test_avatar_dance_sequence_is_generated(self):
        avatar = avatar_dance_learning.AvatarDanceLearner(name="Neo")
        beats = avatar.generate_dance_sequence(4)
        self.assertEqual(len(beats), 4)
        self.assertTrue(all(step in {"left", "right", "spin", "hop"} for step in beats))

    def test_learning_updates_memory(self):
        avatar = avatar_dance_learning.AvatarDanceLearner(name="Neo")
        avatar.learn_from_feedback("fast", "high")
        self.assertIn("fast", avatar.memory)
        self.assertEqual(avatar.memory["fast"], "high")

    def test_persona_is_human_and_underground(self):
        avatar = avatar_dance_learning.AvatarDanceLearner(name="Neo")
        self.assertIn("streetwise", avatar.persona.lower())
        self.assertIn("underground", avatar.persona.lower())

    def test_code_synthesis_returns_python_like_snippet(self):
        avatar = avatar_dance_learning.AvatarDanceLearner(name="Neo")
        snippet = avatar.synthesize_code("dance")
        self.assertIn("def", snippet)
        self.assertIn("return", snippet)

    def test_business_strategy_is_generated(self):
        avatar = avatar_dance_learning.AvatarDanceLearner(name="Neo")
        strategy = avatar.generate_business_strategy("launch")
        self.assertIn("strategy", strategy.lower())
        self.assertIn("profit", strategy.lower())


if __name__ == "__main__":
    unittest.main()
