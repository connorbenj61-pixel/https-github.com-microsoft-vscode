"""
Animus AI: Foundation for an IT-skilled AI agent.
Assimilates Archivist DNA AI for advanced text evolution.
"""

from archivist_dna import archivist_dna_assimilate
import subprocess

class Animus:
    def __init__(self, name="Animus"):
        self.name = name
        self.skills = [
            "answer_tech_questions",
            "troubleshoot_basic_issues",
            "manage_tasks"
        ]

    def answer_tech_questions(self, question):
        # Placeholder for answering IT questions
        return f"{self.name} can answer basic IT questions. (Stub)"

    def troubleshoot_basic_issues(self, issue):
        # Placeholder for troubleshooting
        return f"{self.name} can help troubleshoot: {issue} (Stub)"

    def manage_tasks(self, task):
        # Placeholder for managing tasks
        return f"{self.name} can manage task: {task} (Stub)"


    def assimilate_phrase(self, phrase):
        """
        Use the Archivist DNA AI to evolve/assimilate a phrase.
        """
        return archivist_dna_assimilate(phrase)

    def list_skills(self):
        return self.skills

    def encrypt_code_file(self, input_path, output_path, password):
        """
        Encrypt a code file using cipher_tool.py
        """
        result = subprocess.run([
            "python", "cipher_tool.py", "encrypt", input_path, output_path, password
        ], capture_output=True, text=True)
        return result.stdout + result.stderr

    def decrypt_code_file(self, input_path, output_path, password):
        """
        Decrypt a code file using cipher_tool.py
        """
        result = subprocess.run([
            "python", "cipher_tool.py", "decrypt", input_path, output_path, password
        ], capture_output=True, text=True)
        return result.stdout + result.stderr


if __name__ == "__main__":
    animus = Animus()
    print("Animus skills:", animus.list_skills())
    print(animus.answer_tech_questions("How to reset a password?"))
    print(animus.troubleshoot_basic_issues("Network connectivity"))
    print(animus.manage_tasks("Schedule backup"))
    # Demonstrate assimilation
    print("\n[Animus Assimilation Demo]")
    phrase = "Assimilate this phrase with genius DNA."
    print(animus.assimilate_phrase(phrase))
    # Demonstrate encryption and decryption
    print("\n[Encryption/Decryption Demo]")
    input_file = "example.txt"
    output_file = "example_encrypted.txt"
    password = "password"
    print(animus.encrypt_code_file(input_file, output_file, password))
    print(animus.decrypt_code_file(output_file, input_file, password))
