from typing import List, Optional

from pydantic import BaseModel


class BinaryQuestion(BaseModel):
    topic: str
    difficulty: int
    question: str
    correct_answer: int
    explanation: str


class MultipleChoiceQuestion(BaseModel):
    topic: str
    difficulty: int
    question: str
    correct_answer: str
    wrong_answer1: str
    wrong_answer2: str
    wrong_answer3: str
    explanation: str

class GetQuestion(BaseModel):
    id: int
