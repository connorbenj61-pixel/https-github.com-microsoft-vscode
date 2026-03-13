from dataclasses import dataclass, field

# Legend tiers and their rewards
LEGEND_TIERS = {
    "Bronze": 20,
    "Silver": 40,
    "Gold": 75,
    "Mythic": 150,
    "Eternal": 300
}

# Minimal RitualRecord for demonstration
@dataclass
class RitualRecord:
    player_name: str
    achievement: str
    score: int

@dataclass
class LegendaryRecord(RitualRecord):
    legend_rank: str = "Bronze"
    enshrined_by: str = "Obsidian Heir"

@dataclass
class HallOfLegends:
    legends: list = field(default_factory=list)

    def enshrine(self, record: RitualRecord, rank: str, enshrined_by: str = "Obsidian Heir"):
        reward = LEGEND_TIERS.get(rank, 0)
        legendary = LegendaryRecord(
            **record.__dict__,
            legend_rank=rank,
            enshrined_by=enshrined_by
        )
        self.legends.append(legendary)
        return reward, legendary

# Example usage
if __name__ == "__main__":
    # Create a ritual record
    ritual = RitualRecord(player_name="Alice", achievement="Defeated the Dragon", score=999)

    # Create the Hall of Legends
    hall = HallOfLegends()

    # Enshrine the record as Gold, by the AI Oracle
    reward, legendary = hall.enshrine(ritual, "Gold", "AI Oracle")

    print(f"Reward: {reward} VB")
    print("Legendary Record:")
    print(legendary)
    print("All Legends in Hall:")
    for legend in hall.legends:
        print(legend)
