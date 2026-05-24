import random

class FreudBot:
    def __init__(self, name):
        self.name = name
        self.memory = []

    def respond(self, message):
        # Simple Freud-inspired response logic
        freudisms = [
            "Tell me more about your childhood.",
            "How does that make you feel?",
            "Do you think this relates to your unconscious mind?",
            "Perhaps there is a deeper meaning to your words.",
            "Let's explore your dreams further.",
            "Do you see a connection to your parents?",
            "What do you think this says about your desires?",
            "Is there a hidden wish behind that thought?",
            "How do you interpret this conflict?",
            "Could this be a manifestation of repression?"
        ]
        # Learn from previous message
        self.memory.append(message)
        if len(self.memory) > 1:
            return f"{random.choice(freudisms)} (Reflecting on: '{self.memory[-2]}')"
        else:
            return random.choice(freudisms)


def run_contest(turns=20):
    bot1 = FreudBot("FreudBot_A")
    bot2 = FreudBot("FreudBot_B")
    message = "Let's begin our psychoanalytic contest."
    print("="*40)
    print("FREUD CHATBOT CONTEST: 20/20 SPLIT")
    print("="*40)
    for i in range(turns):
        print(f"\n[FreudBot_A] Turn {i+1}")
        message = bot1.respond(message)
        print(f"A: {message}")
        print(f"\n[FreudBot_B] Turn {i+1}")
        message = bot2.respond(message)
        print(f"B: {message}")
    print("\nContest complete.")

if __name__ == "__main__":
    run_contest(20)
