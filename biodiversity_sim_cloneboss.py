import random

# -------------------------
#  CLEVER CLONE BOSS SIMULATION
# -------------------------

class BioAgent:
    def __init__(self, species, speed, vision, color, behavior):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.color = color
        self.behavior = behavior
        self.surgery_skill = 0.0
        self.surgeries_performed = 0
        self.role = "user"
        self.iq = self.run_iq_test()
        self.machine_code_level = self.learn_machine_code()
        self.virtual_pound = 100  # Every agent starts with 100 virtual pounds

    def act(self):
        return (f"{self.species} ({self.color}) {self.behavior} with speed {self.speed}, vision {self.vision}, "
                f"surgery skill {self.surgery_skill:.2f}, role {self.role}, IQ {self.iq}, "
                f"machine code level {self.machine_code_level}, Virtual Pound £{self.virtual_pound}.")

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

# CloneBoss is created from the cleverest agent(s)
class CloneBoss:
    def __init__(self, agents):
        # Find the cleverest agent(s) by IQ and machine code level
        max_iq = max(a.iq for a in agents)
        max_code = max(a.machine_code_level for a in agents)
        # Try perfect match first
        self.cleverest = [a for a in agents if a.iq == max_iq and a.machine_code_level == max_code]
        if not self.cleverest:
            # If no perfect match, take all with max IQ
            self.cleverest = [a for a in agents if a.iq == max_iq]
            # Assign them to the military
            for a in self.cleverest:
                a.role = "military"
                a.virtual_pound += 50  # Military bonus
        # If still empty, fallback to all with max machine code
        if not self.cleverest:
            self.cleverest = [a for a in agents if a.machine_code_level == max_code]
            for a in self.cleverest:
                a.role = "military"
                a.virtual_pound += 50
        # If still empty, fallback to all agents
        if not self.cleverest:
            self.cleverest = agents
            for a in self.cleverest:
                a.role = "military"
                a.virtual_pound += 50
        # Pick one as the boss
        self.prototype = random.choice(self.cleverest)
        self.name = f"CloneBoss_{self.prototype.species}_{self.prototype.color}"
        self.iq = self.prototype.iq
        self.machine_code_level = self.prototype.machine_code_level
        self.behavior = self.prototype.behavior
        self.role = "boss"
        self.prototype.virtual_pound += 100  # Boss bonus

    def announce(self):
        print(f"{self.name} is the new boss, cloned from the cleverest agent!")
        print(f"IQ: {self.iq}, Machine Code: {self.machine_code_level}, Behavior: {self.behavior}, Role: {self.role}")
        # Announce military members
        print("\nMilitary Members:")
        for agent in self.cleverest:
            print(f"  - {agent.species} ({agent.color}), IQ: {agent.iq}, Machine Code: {agent.machine_code_level}, Role: {agent.role}, Virtual Pound £{agent.virtual_pound}")

def print_balances(agents):
    print("\n--- Virtual Pound Balances ---")
    for agent in agents:
        print(f"{agent.species} ({agent.color}), Role: {agent.role}, Balance: £{agent.virtual_pound}")

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
    print("Clever Clone Boss Simulation\n")
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
    print("\n--- Clone Boss Creation ---\n")
    boss = CloneBoss(population)
    boss.announce()
    print_balances(population)
