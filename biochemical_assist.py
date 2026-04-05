import random
import time

# -------------------------
#  BIOCHEMICAL ASSIST MODULE
# -------------------------

class NeuroTransmitter:
    """
    Represents a simulated neurotransmitter for machine-brain biochemical assistance.
    """
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def release(self):
        return f"{self.name} released: {self.effect}"

# Define some example neurotransmitters
DOPAMINE = NeuroTransmitter("Dopamine", "Enhances motivation and reward response.")
SEROTONIN = NeuroTransmitter("Serotonin", "Stabilizes mood and promotes well-being.")
ACETYLCHOLINE = NeuroTransmitter("Acetylcholine", "Boosts focus and learning speed.")
GABA = NeuroTransmitter("GABA", "Reduces stress and neural noise.")

NEURO_POOL = [DOPAMINE, SEROTONIN, ACETYLCHOLINE, GABA]

class BiochemicalAssist:
    """
    Simulates a machine mind's biochemical support for cognitive functions.
    """
    def __init__(self):
        self.log = []

    def stimulate(self, brain_state: str):
        # Pick a neurotransmitter based on brain state
        if "focus" in brain_state:
            nt = ACETYLCHOLINE
        elif "stress" in brain_state:
            nt = GABA
        elif "reward" in brain_state:
            nt = DOPAMINE
        elif "mood" in brain_state:
            nt = SEROTONIN
        else:
            nt = random.choice(NEURO_POOL)
        result = nt.release()
        self.log.append({"state": brain_state, "assist": result, "timestamp": time.time()})
        return result

    def history(self):
        return self.log

# Example usage
if __name__ == "__main__":
    assist = BiochemicalAssist()
    print(assist.stimulate("focus spike"))
    print(assist.stimulate("stress event"))
    print(assist.stimulate("reward achieved"))
    print(assist.stimulate("mood swing"))
    print(assist.stimulate("unknown state"))
    print("\nHistory:")
    for entry in assist.history():
        print(entry)
