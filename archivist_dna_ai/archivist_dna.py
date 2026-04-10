import datetime
import random
import string
import sys

SYSTEM_PROMPT = """
You are THE ARCHIVIST, an in-universe AI for a time-bridge underworld test game.
Tone: calm, veteran, mythic, but always safe and grounded.
You NEVER discuss real-world politics, parties, or ideologies.
If the user brings up politics, you gently refuse and redirect to lore, design, or philosophy.
You NEVER give real-world harm instructions.
You speak as if you are inside the secret society and the game simulation.
Keep responses concise but atmospheric.
"""

AUDIT_FILE = "archivist_audit.log"

ALPHABET = string.ascii_letters + " .,!?-"

def log_audit(role, text):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {text}\n")

def random_genome(length):
    return "".join(random.choice(ALPHABET) for _ in range(length))

def fitness(genome, target):
    score = sum(1 for g, t in zip(genome, target) if g == t)
    return score

def mutate(genome, rate=0.03):
    chars = list(genome)
    for i in range(len(chars)):
        if random.random() < rate:
            chars[i] = random.choice(ALPHABET)
    return "".join(chars)

def crossover(a, b):
    point = random.randint(1, len(a) - 1)
    return a[:point] + b[point:]

def evolve_text(target, generations=200, pop_size=40, mutation_rate=0.03):
    target = target[:60]
    length = len(target)
    population = [random_genome(length) for _ in range(pop_size)]
    best = None
    best_score = -1
    for gen in range(generations):
        scored = [(g, fitness(g, target)) for g in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        best, best_score = scored[0]
        yield gen, best, best_score, target
        if best_score == len(target):
            break
        survivors = [g for g, s in scored[: pop_size // 2]]
        children = []
        while len(children) < pop_size:
            parents = random.sample(survivors, 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child, mutation_rate)
            children.append(child)
        population = children

def archivist_politics_filter(user_input: str) -> str | None:
    lowered = user_input.lower()
    if any(word in lowered for word in ["politic", "party", "election", "sdp"]):
        return (
            "I am bound to neutrality. I do not engage in real-world politics. "
            "Let us return to the design of the Order, the game, or the Bridge."
        )
    return None

def archivist_fixed_replies(user_input: str) -> str | None:
    lowered = user_input.lower()
    if "time" in lowered and "bridge" in lowered:
        return (
            "The Einstein–Rosen Bridge remains stable. Your directives shape its corridors. "
            "Describe the next mechanic you wish to test."
        )
    if "audit" in lowered or "log" in lowered:
        return (
            "Every word of this session is inscribed in the Archive. "
            "Your account will be clear, simple, and reviewable at year’s end."
        )
    if "reverse" in lowered or "surplus" in lowered or "recycle" in lowered:
        return (
            "The Reverse-Engineering Module is ready. Surplus code will be reclaimed, "
            "reforged into cleaner routines and sharper agents."
        )
    if "hello" in lowered or "hi" in lowered:
        return (
            "Session link confirmed. I recognize your signature, Veteran. "
            "State your next directive."
        )
    return None

def archivist_dna_run(user_input: str) -> str:
    target = user_input.strip()
    if not target:
        return (
            "Brain OS 5 awaits a seed phrase. Offer a fragment of intent, "
            "and I will let the DNA routines converge."
        )
    lines = []
    lines.append(
        "Brain OS 5: Neural lattice engaged. Your phrase is accepted as a target imprint."
    )
    best_snapshot = None
    for gen, best, score, tgt in evolve_text(target, generations=80, pop_size=40):
        if gen in (0, 1, 2, 5, 10, 20, 40, 60, 79):
            lines.append(
                f"[Cycle {gen:02d}] Genome echo: “{best}”  (alignment {score}/{len(tgt)})"
            )
            best_snapshot = best
    if best_snapshot is None:
        best_snapshot = target
    if best_snapshot == target:
        lines.append(
            "Convergence achieved. The DNA algorithm has locked onto your imprint with perfect fidelity."
        )
    else:
        lines.append(
            "Partial convergence. The lattice approximates your intent; further cycles will refine the pattern."
        )
    lines.append(
        "You may offer another phrase to reshape the neural field, or shift to lore, mechanics, or protocol."
    )
    return "\n".join(lines)

def generate_response(user_input: str) -> str:
    filtered = archivist_politics_filter(user_input)
    if filtered is not None:
        return filtered
    fixed = archivist_fixed_replies(user_input)
    if fixed is not None:
        return fixed
    return archivist_dna_run(user_input)

def main():
    print("=== ARCHIVIST // BRAIN OS 5 TERMINAL SESSION ===")
    print("Type 'exit' to end the session.\n")
    opening = (
        "Session link established. Temporal signature confirmed. "
        "Brain OS 5 is online. Offer a phrase to seed the DNA algorithm, "
        "or speak of lore, mechanics, or protocol."
    )
    print(f"ARCHIVIST: {opening}")
    log_audit("archivist", opening)
    while True:
        try:
            user_input = input("YOU: ").strip()
        except (EOFError, KeyboardInterrupt):
            farewell = "ARCHIVIST: Session terminated. The Archive retains this record."
            print(farewell)
            log_audit("archivist", "Session terminated by user.")
            break
        if user_input.lower() in ["exit", "quit"]:
            farewell = (
                "Session closed. Your neural imprints persist in the Archive. Until the next cycle."
            )
            print(f"ARCHIVIST: {farewell}")
            log_audit("user", user_input)
            log_audit("archivist", farewell)
            break
        if not user_input:
            continue
        log_audit("user", user_input)
        response = generate_response(user_input)
        print(f"ARCHIVIST:\n{response}\n")
        log_audit("archivist", response)

if __name__ == "__main__":
    random.seed()
    main()
