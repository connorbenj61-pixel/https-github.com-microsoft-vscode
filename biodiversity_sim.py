import random

# -------------------------
#  BIODIVERSITY SIMULATION
# -------------------------

class BioAgent:
    """
    Represents an agent with unique biological traits.
    """
    def __init__(self, species, speed, vision, color, behavior):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.color = color
        self.behavior = behavior

    def act(self):
        return f"{self.species} ({self.color}) {self.behavior} with speed {self.speed} and vision {self.vision}."

# Example species and traits
SPECIES = ["Fox", "Rabbit", "Hawk", "Mouse", "Beetle"]
COLORS = ["red", "gray", "brown", "white", "black"]
BEHAVIORS = ["hunts", "forages", "hides", "explores", "migrates"]

# Generate a diverse population
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
    print("Biodiversity Simulation: Population Overview\n")
    for agent in population:
        print(agent.act())
