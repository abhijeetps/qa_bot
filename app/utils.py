import json
from typing import List, Dict
from app.models import Question, QuestionList

def load_questions_from_json(file_path: str) -> List[Question]:
    with open(file_path, 'r') as f:
        data = json.load(f)

    questions = QuestionList(**data)
    return questions.questions

def load_json_document(file_path: str) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)
