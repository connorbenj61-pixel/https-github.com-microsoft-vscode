import random

# -------------------------
#  VIRTUAL POKER HOSTING ACROSS EUROPE
# -------------------------

EUROPEAN_CITIES = [
    "London", "Paris", "Berlin", "Madrid", "Rome", "Vienna", "Prague", "Amsterdam", "Brussels", "Budapest"
]

class BioAgent:
    def __init__(self, name, virtual_pound=100):
        self.name = name
        self.virtual_pound = virtual_pound

    def bet(self, amount):
        bet_amount = min(self.virtual_pound, amount)
        self.virtual_pound -= bet_amount
        return bet_amount

    def win(self, amount):
        self.virtual_pound += amount

class VirtualPokerHost:
    def __init__(self, agents):
        self.agents = agents
        self.city = random.choice(EUROPEAN_CITIES)

    def host_game(self):
        print(f"\n--- Virtual Poker Night in {self.city}! ---")
        # Select 4-6 random players
        players = random.sample(self.agents, min(len(self.agents), random.randint(4, 6)))
        print("Players:", ", ".join(a.name for a in players))
        pot = 0
        for player in players:
            bet = player.bet(random.randint(10, 50))
            print(f"{player.name} bets £{bet}")
            pot += bet
        winner = random.choice(players)
        winner.win(pot)
        print(f"{winner.name} wins the pot of £{pot}!")
        print("Balances after game:")
        for player in players:
            print(f"  {player.name}: £{player.virtual_pound}")

if __name__ == "__main__":
    # Example: create 10 agents with names
    agent_names = [
        "Alice", "Bob", "Carla", "Dmitri", "Elena", "Franz", "Greta", "Hugo", "Isabel", "Jasper"
    ]
    agents = [BioAgent(name) for name in agent_names]
    # Host 3 poker games in different cities
    for _ in range(3):
        host = VirtualPokerHost(agents)
        host.host_game()
