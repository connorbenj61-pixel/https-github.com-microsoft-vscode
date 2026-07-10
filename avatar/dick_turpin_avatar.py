from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Avatar:
    """A simple, non-autonomous avatar model.

    This avatar stores descriptive fields and can 'self_improve'
    by adjusting its own attributes (safe, no code execution).
    """
    name: str = "Dick Turpin"
    role: str = "Highwayman (fictional character)"
    personality: str = "roguish, cunning"
    sexuality: str = "unspecified"
    trademark_owner: str = "YourName"
    trademark_label: str = "Dick Turpin Avatar™"

    def describe(self) -> str:
        sex_part = f" Sexuality: {self.sexuality}." if getattr(self, "sexuality", "") else ""
        return (
            f"{self.name} - {self.role}. Personality: {self.personality}.{sex_part}"
        )

    def ascii_art(self) -> str:
        return (
            "  ,--.\n"
            " (  )   .--.  _.._  _.._  .--.\n"
              "  `--'  /    \\`._.`\\`._.`/    \\\n"
              "            `-.__.'  `-`  `-`  `-.__.'\n"
        )

    def self_improve(self, **changes) -> Dict[str, Dict[str, str]]:
        """Safely update avatar attributes. Returns a map of changes.

        Only existing attributes are updated; no code execution or file writes.
        """
        result = {}
        for key, new in changes.items():
            if hasattr(self, key):
                old = getattr(self, key)
                setattr(self, key, new)
                result[key] = {"old": str(old), "new": str(new)}
        return result

    def trademark_notice(self) -> str:
        return (
            f"© 2026 {self.trademark_owner}. All rights reserved. \"{self.trademark_label}\"\n"
            "(This is a placeholder notice for TM testing - not a legal registration.)"
        )

    def to_dict(self) -> Dict:
        return asdict(self)
