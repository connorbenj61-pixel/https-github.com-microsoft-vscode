"""
Animus AI: Foundation for an IT-skilled AI agent.
"""

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

    def list_skills(self):
        return self.skills

if __name__ == "__main__":
    animus = Animus()
    print("Animus skills:", animus.list_skills())
    print(animus.answer_tech_questions("How to reset a password?"))
    print(animus.troubleshoot_basic_issues("Network connectivity"))
    print(animus.manage_tasks("Schedule backup"))
