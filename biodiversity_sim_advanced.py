import random

# -------------------------
#  ADVANCED BIODIVERSITY SIMULATION WITH PSEUDO SURGERY
# -------------------------

class BioAgent:
    """
    Represents an agent with unique biological traits and the ability to learn pseudo surgery.
    """
    def __init__(self, species, speed, vision, color, behavior):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.color = color
        self.behavior = behavior
        self.surgery_skill = 0.0  # Skill level from 0.0 to 1.0
        self.surgeries_performed = 0

    def act(self):
        return f"{self.species} ({self.color}) {self.behavior} with speed {self.speed}, vision {self.vision}, surgery skill {self.surgery_skill:.2f}."

    def attempt_surgery(self, patient):
        """
        Simulate a pseudo surgery attempt on another agent.
        Success depends on skill and randomness.
        """
        difficulty = random.uniform(0.2, 0.8)
        outcome = self.surgery_skill + random.uniform(-0.2, 0.2) > difficulty
        if outcome:
            self.surgery_skill = min(1.0, self.surgery_skill + 0.05)
            self.surgeries_performed += 1
            return f"{self.species} successfully performed pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."
        else:
            self.surgery_skill = max(0.0, self.surgery_skill - 0.02)
            return f"{self.species} failed pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."

# Example species and traits
SPECIES = ["Fox", "Rabbit", "Hawk", "Mouse", "Beetle"]
COLORS = ["red", "gray", "brown", "white", "black"]
BEHAVIORS = ["hunts", "forages", "hides", "explores", "migrates"]

POPULATION_SIZE = 20

def create_population(size=POPULATION_SIZE):
    population = []
    for _ in range(size):
        species = random.choice(SPECIES)
        speed = round(random.uniform(1.0, 10.0), 2)
        vision = round(random.uniform(1.0, 10.0), 2)
        color = random.choice(COLORS)
        behavior = random.choice(BEHAVIORS)
        agent = BioAgent(species, speed, vision, color, behavior)
        population.append(agent)
    return population

if __name__ == "__main__":
    population = create_population()
    print("Advanced Biodiversity Simulation: Pseudo Surgery\n")
    for agent in population:
        print(agent.act())
    print("\n--- Pseudo Surgery Attempts ---\n")
    for _ in range(10):
        surgeon = random.choice(population)
        patient = random.choice([a for a in population if a != surgeon])
        print(surgeon.attempt_surgery(patient))
