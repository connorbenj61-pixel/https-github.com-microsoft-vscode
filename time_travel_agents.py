import random

# -------------------------
#  TIME TRAVEL AGENT SIMULATION
# -------------------------

class TimeTravelAgent:
    def __init__(self, name, start_year=2026, virtual_pound=100):
        self.name = name
        self.current_year = start_year
        self.virtual_pound = virtual_pound
        self.time_travel_history = [start_year]
        self.time_stability = 100  # 0-100, decreases with paradoxes or risky jumps

    def time_travel(self, target_year):
        print(f"{self.name} time travels from {self.current_year} to {target_year}!")
        # Paradox detection: visiting the same year twice in a row
        if self.current_year == target_year:
            print(f"  [PARADOX] {self.name} tried to visit the same year twice in a row!")
            self.time_stability -= 20
            self.virtual_pound = max(0, self.virtual_pound - 10)
        # Self-meeting: if agent has already visited this year (not in a row)
        elif target_year in self.time_travel_history:
            print(f"  [SELF-MEETING] {self.name} meets their past/future self in {target_year}!")
            self.virtual_pound += 20
            self.time_stability -= 10
        # Risky jump: large time jump
        jump_size = abs(target_year - self.current_year)
        if jump_size > 200:
            print(f"  [RISKY JUMP] {self.name} made a risky jump of {jump_size} years!")
            self.time_stability -= 15
            self.virtual_pound = max(0, self.virtual_pound - 15)
        # Clever jump: to a year ending in 0 or 5
        if target_year % 5 == 0:
            print(f"  [CLEVER JUMP] {self.name} jumped to a round year!")
            self.virtual_pound += 10
        self.current_year = target_year
        self.time_travel_history.append(target_year)
        # Standard cost
        cost = jump_size // 10
        self.virtual_pound = max(0, self.virtual_pound - cost)
        # Clamp stability
        self.time_stability = max(0, min(100, self.time_stability))
        print(f"{self.name} now has £{self.virtual_pound} and time stability {self.time_stability} after time travel.\n")

    def show_history(self):
        print(f"{self.name}'s time travel history: {self.time_travel_history}")
        print(f"{self.name}'s final virtual pound: £{self.virtual_pound}, time stability: {self.time_stability}\n")

if __name__ == "__main__":
    agents = [TimeTravelAgent(f"Agent_{i+1}") for i in range(5)]
    for agent in agents:
        # Each agent makes 3 random time jumps
        for _ in range(3):
            jump = random.choice([-100, -50, -10, 10, 50, 100, 500])
            agent.time_travel(agent.current_year + jump)
        agent.show_history()
