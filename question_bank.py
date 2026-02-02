import random
import json
import os

class QuestionBank:
    def __init__(self, questions_file, used_file="used_questions.json"):
        self.questions_file = questions_file
        self.used_file = used_file
        self.questions = self._load_questions()
        self.used_questions = self._load_used_questions()

    def _load_questions(self):
        with open(self.questions_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
        
    def _load_used_questions(self):
        if os.path.exists(self.used_file):
            with open(self.used_file, "r", encoding="utf-8") as f:
                return set(json.load(f))
        return set()
    
    def _saved_used_questions(self):
        with open(self.used_file, "w", encoding="utf-8") as f:
            json.dump(list(self.used_questions), f, ensure_ascii=False, indent=2)

    def get_random_unused_question(self):
        available = list(set(self.questions) - self.used_questions)

        if not available:
            raise Exception("Semua soal sudah dipakai!")
        
        question = random.choice(available)
        self.used_questions.add(question)
        self._saved_used_questions()

        return question