import random

class PsychiatristBot:
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.questions = [
            "Can you tell me how you've been feeling lately?",
            "Have you experienced any unusual thoughts or beliefs?",
            "Do you ever hear or see things that others do not?",
            "How is your sleep and appetite?",
            "Do you feel that people are watching or controlling you?",
            "Can you describe your mood today?",
            "Do you have trouble concentrating or remembering things?",
            "Have you noticed any changes in your behavior?",
            "Do you feel safe?",
            "Is there anything else you want to share with me today?"
        ]
    def respond(self, message):
        self.memory.append(message)
        # Ask a new question, sometimes referencing the patient's last answer
        if len(self.memory) > 1:
            return f"{random.choice(self.questions)} (Earlier you said: '{self.memory[-2]}')"
        else:
            return random.choice(self.questions)

class SchizophreniaPatientBot:
    def __init__(self, name):
        self.name = name
        self.memory = []
        self.responses = [
            "Sometimes I hear voices telling me things...",
            "I think the TV is sending me secret messages.",
            "I can't sleep, my mind is too busy.",
            "People are following me, I know it.",
            "My thoughts get all jumbled up sometimes.",
            "I feel like my food is being poisoned.",
            "I see shadows moving in the corners.",
            "I forget things a lot, even simple things.",
            "I feel scared, but I don't know why.",
            "Sometimes I feel like I'm not real."
        ]
    def respond(self, message):
        self.memory.append(message)
        # Respond with a symptom or delusional thought, sometimes referencing the psychiatrist's last question
        if len(self.memory) > 1:
            return f"{random.choice(self.responses)} (About your question: '{self.memory[-2]}')"
        else:
            return random.choice(self.responses)

def run_psychiatry_session(turns=10):
    psychiatrist = PsychiatristBot("Dr. Freud")
    patient = SchizophreniaPatientBot("Patient X")
    message = "Hello, I'm here to help you."
    print("="*50)
    print("PSYCHIATRIST vs SCHIZOPHRENIA PATIENT SESSION")
    print("="*50)
    for i in range(turns):
        print(f"\n[Dr. Freud] Turn {i+1}")
        message = psychiatrist.respond(message)
        print(f"Psychiatrist: {message}")
        print(f"\n[Patient X] Turn {i+1}")
        message = patient.respond(message)
        print(f"Patient: {message}")
    print("\nSession complete.")

if __name__ == "__main__":
    run_psychiatry_session(10)
