#!/usr/bin/env python3
"""Demo runner for the Dick Turpin avatar.

Shows description, ascii art, trademark notice, and a safe self-improvement step.
"""
from avatar.dick_turpin_avatar import Avatar


def main():
    a = Avatar()
    print("Avatar description:")
    print(a.describe())
    print()
    print("Avatar ASCII art (stylized):")
    print(a.ascii_art())
    print()
    print("Trademark notice:")
    print(a.trademark_notice())
    print()
    print("Applying a safe self_improve update (personality + sexuality tweak)...")
    changes = a.self_improve(personality="brooding, theatrical", sexuality="heterosexual (straight)")
    print("Changes:", changes)
    print()
    print("Updated description:")
    print(a.describe())


if __name__ == "__main__":
    main()
