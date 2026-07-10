#!/usr/bin/env python3
"""Run a simple AI World Cup simulator.

Creates groups, runs group stage, then knockout rounds and prints the champion.
"""
import argparse
import random
from pathlib import Path

from world_cup_ai.ai_team import Team
from world_cup_ai.engine import play_group, play_knockout


DEFAULT_TEAMS = [
    "Aland", "Borealia", "Cyrenia", "Deltora", "Eldoria", "Freedon", "Galdor", "Hesper",
    "Ionia", "Jorvik", "Kordia", "Lunaria", "Maris", "Nerath", "Orion", "Pereus",
]


def make_teams(names, rng: random.Random, horror: bool = False):
    teams = []
    horror_suffixes = ["Wraiths", "Nightmares", "Shades", "Spectres", "Abyss"]
    for i, n in enumerate(names):
        base_name = n
        if horror:
            # create a darker team name
            suffix = rng.choice(horror_suffixes)
            base_name = f"{n} {suffix}"
        strength = rng.uniform(40, 95)
        style = rng.choice(["balanced", "attacking", "defensive"])
        teams.append(Team(base_name, strength, style))
    return teams


def run_tournament(teams, seed=None, verbose=False):
    rng = random.Random(seed)
    rng.shuffle(teams)

    num_groups = len(teams) // 4
    groups = [teams[i * 4:(i + 1) * 4] for i in range(num_groups)]

    if verbose:
        print("Groups:")
        for i, g in enumerate(groups, 1):
            print(f" Group {i}: {', '.join(map(str, g))}")
        print()

    qualified = []
    for g in groups:
        table = play_group(g)
        if verbose:
            print("Group results:")
            for r in table:
                t = r["team"]
                print(f"  {t.name}: pts={r['pts']} gd={r['gd']} gf={r['gf']}")
            print()
        # top two advance
        qualified.append(table[0]["team"])
        qualified.append(table[1]["team"])

    # knockout bracket: shuffle qualified teams
    rng.shuffle(qualified)
    if verbose:
        print("Knockout qualifiers:")
        print(", ".join(t.name for t in qualified))
        print()

    # quarterfinals -> semis -> final
    round_teams = qualified
    round_names = ["Round of 16", "Quarterfinals", "Semifinals", "Final"]
    while len(round_teams) > 1:
        next_round = []
        for i in range(0, len(round_teams), 2):
            a = round_teams[i]
            b = round_teams[i + 1]
            winner = play_knockout(a, b)
            if verbose:
                print(f"{a.name} vs {b.name} -> {winner.name}")
        
            next_round.append(winner)
        round_teams = next_round
    champion = round_teams[0]
    return champion


def main():
    parser = argparse.ArgumentParser(description="AI World Cup simulator")
    parser.add_argument("--teams", nargs="*", help="Team names (default set used if omitted)")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--horror", action="store_true", help="Enable horror-themed mode (non-graphic)")
    args = parser.parse_args()

    names = args.teams or DEFAULT_TEAMS
    teams = make_teams(names, random, horror=args.horror)
    if args.horror:
        print("\n--- HORROR MODE: human equivalent atmosphere enabled ---\n")
    champ = run_tournament(teams, seed=args.seed, verbose=args.verbose)
    print(f"\nChampion: {champ.name} (strength {champ.strength:.0f})")
    if args.horror:
        # simple trademark-style line (placeholder)
        print("\n© 2026 YourName. All rights reserved. 'AI World Cup: Human Nightmares'™ (placeholder). Replace with your legal trademark details.")


if __name__ == "__main__":
    main()
