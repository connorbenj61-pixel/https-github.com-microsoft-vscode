# Archivist DNA AI - Shared Module for Assimilation
import datetime
import random
import string

AUDIT_FILE = "archivist_audit.log"
ALPHABET = string.ascii_letters + " .,!?-"

def log_audit(role, text):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {role.upper()}: {text}\n")

def random_genome(length):
    return "".join(random.choice(ALPHABET) for _ in range(length))

def fitness(genome, target):
    return sum(1 for g, t in zip(genome, target) if g == t)

def mutate(genome, rate):
    chars = list(genome)
    for i in range(len(chars)):
        if random.random() < rate:
            chars[i] = random.choice(ALPHABET)
    return "".join(chars)

def crossover(a, b):
    point = random.randint(1, len(a) - 1)
    return a[:point] + b[point:]

def evolve_text(target, generations=80, pop_size=40, mutation_rate=0.03):
    target = target[:60]
    length = len(target)
    population = [random_genome(length) for _ in range(pop_size)]
    best = None
    best_score = -1
    for gen in range(generations):
        scored = [(g, fitness(g, target)) for g in population]
        scored.sort(key=lambda x: x[1], reverse=True)
        best, best_score = scored[0]
        adaptive_mutation = max(0.01, mutation_rate * (1 - best_score / max(1, len(target))))
        yield gen, best, best_score, target, adaptive_mutation
        if best_score == len(target):
            break
        next_population = [best]
        survivors = [g for g, s in scored[: pop_size // 2]]
        while len(next_population) < pop_size:
            parents = random.sample(survivors, 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child, adaptive_mutation)
            next_population.append(child)
        population = next_population

def archivist_dna_assimilate(text):
    """
    Assimilate a phrase using the Archivist's DNA algorithm and return the evolution log.
    """
    lines = []
    lines.append("[Assimilation] Brain OS 5: Neural lattice engaged. Assimilating phrase...")
    best_snapshot = None
    for gen, best, score, tgt, mut in evolve_text(text, generations=80, pop_size=40):
        if gen in (0, 1, 2, 5, 10, 20, 40, 60, 79):
            lines.append(f"[Cycle {gen:02d}] Genome echo: “{best}”  (alignment {score}/{len(tgt)}) | mutation rate: {mut:.4f}")
            best_snapshot = best
    if best_snapshot == text:
        lines.append("[Assimilation] Genius convergence achieved. (IQ: 233)")
    else:
        lines.append("[Assimilation] Partial convergence. Further cycles will refine the pattern. (IQ: 233)")
    return "\n".join(lines)
