import random

# -------------------------
#  AVATAR BOSS & GENIUS CLUB IQ MACHINE
# -------------------------

class BioAgent:
    """
    Represents an agent with unique biological traits, the ability to learn pseudo surgery, a role (user/administrator), IQ, and machine code understanding.
    """
    def __init__(self, species, speed, vision, color, behavior):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.color = color
        self.behavior = behavior
        self.surgery_skill = 0.0  # Skill level from 0.0 to 1.0
        self.surgeries_performed = 0
        self.role = "user"  # Default role
        self.iq = self.run_iq_test()
        self.machine_code_level = self.learn_machine_code()

    def act(self):
        return (f"{self.species} ({self.color}) {self.behavior} with speed {self.speed}, vision {self.vision}, "
                f"surgery skill {self.surgery_skill:.2f}, role {self.role}, IQ {self.iq}, "
                f"machine code level {self.machine_code_level}.")

    def attempt_surgery(self, patient):
        difficulty = random.uniform(0.2, 0.8)
        outcome = self.surgery_skill + random.uniform(-0.2, 0.2) > difficulty
        if outcome:
            self.surgery_skill = min(1.0, self.surgery_skill + 0.05)
            self.surgeries_performed += 1
            if self.surgery_skill > 0.7 and self.role != "administrator":
                self.role = "administrator"
                return f"{self.species} promoted to administrator after successful pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."
            return f"{self.species} successfully performed pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."
        else:
            self.surgery_skill = max(0.0, self.surgery_skill - 0.02)
            if self.role == "administrator" and self.surgery_skill < 0.5:
                self.role = "user"
                return f"{self.species} demoted to user after failed pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."
            return f"{self.species} failed pseudo surgery on {patient.species}. Skill now {self.surgery_skill:.2f}."

    def run_iq_test(self):
        base = 80 + int(self.vision + self.speed)
        bonus = 10 if self.behavior == "explores" else 0
        randomness = random.randint(-10, 20)
        return base + bonus + randomness

    def learn_machine_code(self):
        base = 0
        if self.iq > 110:
            base += 1
        if self.behavior == "explores":
            base += 1
        if self.iq > 120:
            base += 1
        return min(base, 3)

# Avatar Boss controls the IQ machine and Genius Club
class AvatarBoss:
    def __init__(self, name="Avatar Boss"):
        self.name = name
        self.genius_club = []  # Only agents with IQ >= 120
        self.iq_machine_programmers = []

    def evaluate_agents(self, agents):
        self.genius_club = [a for a in agents if a.iq >= 120]
        self.iq_machine_programmers = [a for a in self.genius_club if a.machine_code_level >= 2]

    def announce(self):
        print(f"{self.name} presides over the Genius Club!")
        print(f"Genius Club Members (IQ >= 120): {len(self.genius_club)}")
        for agent in self.genius_club:
            print(f"  - {agent.species} ({agent.color}), IQ: {agent.iq}, Machine Code: {agent.machine_code_level}")
        print(f"\nIQ Machine Programmers (Genius + Machine Code >= 2): {len(self.iq_machine_programmers)}")
        for agent in self.iq_machine_programmers:
            print(f"  - {agent.species} ({agent.color}), IQ: {agent.iq}, Machine Code: {agent.machine_code_level}")

    def run_iq_machine(self):
        print(f"\n{self.name} runs the IQ Machine, programmed by the Genius Club only!")
        if not self.iq_machine_programmers:
            print("No eligible programmers. IQ Machine is idle.")
        else:
            for agent in self.iq_machine_programmers:
                print(f"IQ Machine programmed by {agent.species} ({agent.color}) with IQ {agent.iq} and Machine Code {agent.machine_code_level}.")

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
    print("Avatar Boss & Genius Club IQ Machine Simulation\n")
    for agent in population:
        print(agent.act())
    print("\n--- Pseudo Surgery Attempts ---\n")
    for _ in range(10):
        surgeon = random.choice(population)
        patient = random.choice([a for a in population if a != surgeon])
        print(surgeon.attempt_surgery(patient))
    print("\n--- Final Agent States ---\n")
    for agent in population:
        print(agent.act())
    print("\n--- Avatar Boss Evaluation ---\n")
    boss = AvatarBoss()
    boss.evaluate_agents(population)
    boss.announce()
    boss.run_iq_machine()
