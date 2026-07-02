import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import upgrade_console


class UpgradeConsoleTests(unittest.TestCase):
    def test_resolve_repo_target_uses_fallback_when_empty(self):
        fallback_path = os.path.abspath("/tmp/fallback")
        self.assertEqual(upgrade_console.resolve_repo_target("", fallback_path), fallback_path)
        self.assertEqual(upgrade_console.resolve_repo_target("   ", fallback_path), fallback_path)

    def test_resolve_repo_target_keeps_requested_path(self):
        requested_path = os.path.abspath("/tmp/custom")
        self.assertEqual(
            upgrade_console.resolve_repo_target(requested_path, os.path.abspath("/tmp/fallback")),
            requested_path,
        )

    def test_build_git_command_prefixes_git(self):
        self.assertEqual(
            upgrade_console.build_git_command(["clone", "https://example.com/repo"]),
            ["git", "clone", "https://example.com/repo"],
        )

    def test_should_use_terminal_mode_when_forced(self):
        self.assertTrue(upgrade_console.should_use_terminal_mode(force_terminal=True))

    def test_should_use_terminal_mode_when_display_missing(self):
        self.assertTrue(
            upgrade_console.should_use_terminal_mode(force_terminal=False, environment={"DISPLAY": ""})
        )


if __name__ == "__main__":
    unittest.main()
