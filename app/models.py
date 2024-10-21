from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    text: str

class QuestionList(BaseModel):
    questions: List[Question]

class Answer(BaseModel):
    question: str
    answer: str

class AnswerList(BaseModel):
    answers: List[Answer]

class QuestionRequest(BaseModel):
    questions: List[Question]
