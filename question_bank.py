import random

class QuestionBank:
    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = self._load_questions()

    def _load_questions(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
        
    def get_random_question(self):
        return random.choice(self.questions)
