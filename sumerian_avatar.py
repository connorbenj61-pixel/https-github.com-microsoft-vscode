"""
Sumerian XNOR Pilot Avatar
A virtual assistant inspired by ancient Sumerian lore and digital logic.
"""


import random
import math

class QuantumSumerianAIPilot:
    def __init__(self, name="ENKI-QUANTUM"):
        self.name = name
        self.lore = (
            f"{self.name} is a quantum synthetic avatar, modeled after the wisdom of ancient Sumerian pilots. "
            "It communicates using natural language, symbolic logic, and quantum logic, harnessing the power of superposition and entanglement."
        )

    def introduce(self):
        return f"I am {self.name}, your quantum Sumerian pilot. {self.lore}"

    def xnor_logic(self, a: int, b: int) -> int:
        """Simulate XNOR logic (returns 1 if a and b are the same, else 0)."""
        return int(a == b)

    def quantum_superposition(self):
        """Simulate a quantum superposition (returns a random qubit state)."""
        alpha = random.random()
        beta = math.sqrt(1 - alpha ** 2)
        return f"|ψ⟩ = {alpha:.2f}|0⟩ + {beta:.2f}|1⟩"

    def quantum_entanglement(self):
        """Simulate a quantum entanglement state."""
        return "|Φ+⟩ = (|00⟩ + |11⟩)/√2 — Entangled across realms!"

    def respond(self, message: str) -> str:
        msg = message.lower()
        if "xnor" in msg:
            return "XNOR is the logic of equivalence. Provide two bits (0 or 1) to compute."
        elif "superposition" in msg:
            return f"Quantum superposition: {self.quantum_superposition()}"
        elif "entangle" in msg or "entanglement" in msg:
            return f"Quantum entanglement: {self.quantum_entanglement()}"
        elif "lore" in msg:
            return self.lore
        elif "pilot" in msg:
            return "Navigating quantum, digital, and ancient realms alike."
        elif "quantum" in msg:
            return "Quantum logic enables me to exist in many states at once. Ask about superposition or entanglement!"
        else:
            return f"{self.name} acknowledges: {message}"

if __name__ == "__main__":
    avatar = QuantumSumerianAIPilot()
    print(avatar.introduce())
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Farewell, traveler.")
            break
        elif user_input.lower().startswith("xnor"):
            try:
                _, a, b = user_input.split()
                result = avatar.xnor_logic(int(a), int(b))
                print(f"XNOR({a}, {b}) = {result}")
            except Exception:
                print("Usage: xnor 0 1")
        else:
            print(avatar.respond(user_input))
