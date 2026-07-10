import random
from typing import List, Tuple
from .ai_team import Team


def simulate_goals(mean: float) -> int:
    # simple stochastic goals model: Gaussian around mean, min 0
    g = int(max(0, round(random.gauss(mean, max(0.8, mean * 0.35)))))
    return g


def simulate_match(a: Team, b: Team, neutral: bool = True) -> Tuple[int, int]:
    # compute base expected goals from strengths
    total = a.strength + b.strength
    if total <= 0:
        total = 1.0
    a_expect = 1.0 + 2.0 * (a.strength / total)
    b_expect = 1.0 + 2.0 * (b.strength / total)

    # style modifiers
    if a.style == "attacking":
        a_expect *= 1.1
    if b.style == "attacking":
        b_expect *= 1.1
    if a.style == "defensive":
        a_expect *= 0.9
    if b.style == "defensive":
        b_expect *= 0.9

    # home advantage
    if not neutral:
        a_expect *= 1.05

    a_goals = simulate_goals(a_expect)
    b_goals = simulate_goals(b_expect)
    return a_goals, b_goals


def play_group(teams: List[Team]) -> List[dict]:
    # round-robin: points, gd, goals
    table = {t.name: {"team": t, "pts": 0, "gd": 0, "gf": 0} for t in teams}
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            a = teams[i]
            b = teams[j]
            ga, gb = simulate_match(a, b)
            if ga > gb:
                table[a.name]["pts"] += 3
            elif gb > ga:
                table[b.name]["pts"] += 3
            else:
                table[a.name]["pts"] += 1
                table[b.name]["pts"] += 1
            table[a.name]["gf"] += ga
            table[b.name]["gf"] += gb
            table[a.name]["gd"] += ga - gb
            table[b.name]["gd"] += gb - ga

    rows = list(table.values())
    rows.sort(key=lambda r: (r["pts"], r["gd"], r["gf"]), reverse=True)
    return rows


def play_knockout(a: Team, b: Team) -> Team:
    ga, gb = simulate_match(a, b)
    if ga != gb:
        return a if ga > gb else b
    # extra-time (simulated boost)
    ga2, gb2 = simulate_match(a, b)
    if ga2 != gb2:
        return a if ga2 > gb2 else b
    # penalties: random weighted by strength
    weights = [a.strength, b.strength]
    winner = random.choices([a, b], weights=weights, k=1)[0]
    return winner
