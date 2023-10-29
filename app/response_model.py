from typing import List, Optional, Dict, Any

import fastapi
from pydantic import BaseModel


class BinaryQuestion(BaseModel):
    topic: str
    difficulty: int
    question: str
    correct_answer: int
    explanation: str
    example: str


class BinaryQuestions(BaseModel):
    data: List[BinaryQuestion]

class TopicName(BaseModel):
    topic: str

class UploadFile(BaseModel):
    topic: str
    file: str

class MultipleChoiceQuestion(BaseModel):
    topic: str
    difficulty: int
    question: str
    correct_answer: str
    wrong_answer1: str
    wrong_answer2: str
    wrong_answer3: str
    explanation: str
    explanation: str

class GetQuestion(BaseModel):
    id: int

class GetBinaryQuestionsByTopicAndDifficulty(BaseModel):
    topic: str
    difficulty: int

class CreateQuestionModelWithTopic(BaseModel):
    profile: str
    intent: str
    topic: str


class CreateQuestionModelWithPdf(BaseModel):
    profile: str
    intent: str
    pdf_file: fastapi.UploadFile


class ReinforceTopicModel(BaseModel):
    topics: List[str]


class ReinforceAutoModel(BaseModel):
    correct_responses: List[int]
    incorrect_responses: List[int]


class QuestionsList(BaseModel):
    data: List[Dict[str, Any]]