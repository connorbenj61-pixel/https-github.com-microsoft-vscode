import unittest

# Dummy chatbot function for demonstration
def chatbot_response(prompt):
    # Improved detection for self-dialogue prompts
    self_keywords = [
        'your own', 'yourself', 'you', 'AI', 'performance', 'purpose', 'limitations', 'improve', 'errors', 'logic'
    ]
    if any(word in prompt.lower() for word in self_keywords):
        return "Self-dialogue: AI reflecting on itself."
    return "User-dialogue: AI responding to user."

class TestChatbotSelfTesting(unittest.TestCase):
    def setUp(self):
        # 50% self-generated prompts, 50% user prompts
        self.self_prompts = [
            "How do you evaluate your own performance?",
            "What is your purpose as an AI?",
            "Can you improve yourself?",
            "Describe your own limitations.",
            "How do you handle errors in your logic?"
        ]
        self.user_prompts = [
            "What is the weather today?",
            "Tell me a joke.",
            "How do I reset my password?",
            "What is the capital of France?",
            "Translate 'hello' to Spanish."
        ]

    def test_self_dialogue(self):
        for prompt in self.self_prompts:
            response = chatbot_response(prompt)
            self.assertIn("Self-dialogue", response)

    def test_user_dialogue(self):
        for prompt in self.user_prompts:
            response = chatbot_response(prompt)
            self.assertIn("User-dialogue", response)

if __name__ == "__main__":
    unittest.main()
