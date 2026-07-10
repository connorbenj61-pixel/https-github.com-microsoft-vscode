from dataclasses import dataclass


@dataclass
class Team:
    name: str
    strength: float  # 1.0 - 100.0, higher is better
    style: str = "balanced"  # defensive, attacking, balanced

    def __repr__(self) -> str:
        return f"{self.name}({self.strength:.0f})"
