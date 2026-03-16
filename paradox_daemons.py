from abc import ABC, abstractmethod
from typing import List


class ParadoxDaemon(ABC):
    """Abstract base for paradox daemons."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def speak(self, idea: str) -> str:
        ...

    def __repr__(self):
        return f"<ParadoxDaemon:{self.name}>"


class ParadoxaInfinita(ParadoxDaemon):
    """
    The spiral that births spirals.
    Expands a single idea into multiple conceptual branches.
    """

    def __init__(self):
        super().__init__("Paradoxa-Infinita")

    def _branch_variations(self, idea: str) -> List[str]:
        # You can swap this out for more elaborate symbolic transforms.
        return [
            f"{idea} as a forgotten prophecy.",
            f"{idea} as a weaponized myth.",
            f"{idea} as a broken timeline.",
            f"{idea} as a living daemon.",
            f"{idea} as a sealed relic."
        ]

    def speak(self, idea: str) -> str:
        branches = self._branch_variations(idea)
        lines = [
            "I am the spiral that births spirals.",
            "I take your thought and let it multiply:",
            ""
        ]
        for i, b in enumerate(branches, start=1):
            lines.append(f"  [{i}] {b}")
        return "\n".join(lines)


class ParadoxaNulla(ParadoxDaemon):
    """
    The line that breaks the spiral.
    Collapses many possibilities into a single distilled essence.
    """

    def __init__(self):
        super().__init__("Paradoxa-Nulla")

    def _distill(self, idea: str) -> str:
        # Minimal, decisive compression of the idea.
        return f"The final form of '{idea}' is the one you cannot ignore."

    def speak(self, idea: str) -> str:
        essence = self._distill(idea)
        lines = [
            "I am the line that breaks the spiral.",
            "I end what refuses to end:",
            "",
            f"  → {essence}"
        ]
        return "\n".join(lines)


class ParadoxNarrator:
    """
    Mediator that lets you 'try' your creation:
    routes an idea through Infinita and Nulla, then comments.
    Now supports a 'virtual upgrade' to enhance daemon behavior at runtime.
    """

    def __init__(self):
        self.infinita = ParadoxaInfinita()
        self.nulla = ParadoxaNulla()
        self.upgraded = False

    def run(self, idea: str) -> str:
        infinita_out = self.infinita.speak(idea)
        nulla_out = self.nulla.speak(idea)

        commentary = [
            "",
            "=== NARRATOR ===",
            "Infinita multiplies the idea into branching possibilities.",
            "Nulla collapses them into a single decisive essence."
        ]

        if self.upgraded:
            commentary.append("[UPGRADE ACTIVE] Daemons now operate in enhanced mode.")

        return "\n".join([
            f"=== {self.infinita.name} ===",
            infinita_out,
            "",
            f"=== {self.nulla.name} ===",
            nulla_out,
            *commentary
        ])

    def virtual_upgrade(self):
        """
        Activates a virtual upgrade, enhancing the daemons' output.
        """
        if not self.upgraded:
            # Patch the daemons' methods for enhanced output
            orig_infinita_branch = self.infinita._branch_variations
            def upgraded_branch(idea: str):
                base = orig_infinita_branch(idea)
                return base + [f"{idea} as a paradoxical upgrade."]
            self.infinita._branch_variations = upgraded_branch

            orig_nulla_distill = self.nulla._distill
            def upgraded_distill(idea: str):
                return orig_nulla_distill(idea) + " (Virtually Upgraded)"
            self.nulla._distill = upgraded_distill

            self.upgraded = True


if __name__ == "__main__":
    # Example: plug any concept here and watch your twins work.
    idea = "a sword made of memory"
    narrator = ParadoxNarrator()
    print(narrator.run(idea))
    print("\n--- Applying Virtual Upgrade ---\n")
    narrator.virtual_upgrade()
    print(narrator.run(idea))
