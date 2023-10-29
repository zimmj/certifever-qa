import logging
from pathlib import Path
from typing import Annotated

from omegaconf import OmegaConf
from fastapi import FastAPI, Depends, HTTPException

from app.db.database import SessionLocal, engine, Base
import app.response_model as model
from app.db.crud import BinaryQuestionRepo

logger = logging.getLogger(__name__)
server = FastAPI()
ENDPOINTS_FILE = Path(__file__).parent.resolve() / "endpoints.yaml"
ENDPOINTS = OmegaConf.load(ENDPOINTS_FILE)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_binary_question_repo(db=Depends(get_db)):
    return BinaryQuestionRepo(db)


@server.on_event("startup")
async def startup_event():
    # Create the database tables
    Base.metadata.create_all(bind=engine)


@server.get(ENDPOINTS.root.path)
def root():
    return {"message": "AI Prompter Server is running"}


mock_questions_list = model.QuestionsList(
    data=[
        {
            "question": "blablabla",
            "options": [
                "AAA",
                "BBB",
                "CCC",
                "DDD"
            ],

            "correct_answer_id": 2,
            "explanation": "short explanation of the correct answer in one short sentence",
            "topic": "topic"
        },
        {
            "question": "blablabla_2",
            "options": [
                "AAA",
                "BBB",
                "CCC",
                "DDD"
            ],

            "correct_answer_id": 2,
            "explanation": "short explanation of the correct answer in one short sentence",
            "topic": "topic"
        },
    ]
)


@server.post(ENDPOINTS.create_questions_with_topic.path, response_model=model.QuestionsList)
def create_questions_with_topic(
        create_question_model: Annotated[model.CreateQuestionModelWithTopic, Depends()],
):
    # call GPTPrompter to generate questions

    # mock it here
    return mock_questions_list


@server.post(ENDPOINTS.create_questions_with_pdf.path, response_model=model.QuestionsList)
def create_questions_with_pdf(
        create_question_model: Annotated[model.CreateQuestionModelWithPdf, Depends()],
):
    # call GPTPrompter to generate questions

    # mock it here
    return mock_questions_list


@server.post(ENDPOINTS.reinforce_on_topics.path, response_model=model.QuestionsList)
def reinforce_on_topics(
        reinforcement_topics: Annotated[model.ReinforceTopicModel, Depends()],
):
    # call GPTPrompter to reinforce on topics

    # mocking it here
    return mock_questions_list


@server.post(ENDPOINTS.reinforce_auto.path, response_model=model.QuestionsList)
def reinforce_auto(
        reinforcement_auto: Annotated[model.ReinforceAutoModel, Depends()],
):
    # call GPTPrompter to reinforce automatically based on user's performance

    # mocking it here
    return mock_questions_list


@server.post(ENDPOINTS.adjust_difficulty.path, response_model=model.QuestionsList)
def adjust_difficulty(
        adjust_difficulty: Annotated[model.AdjustDifficultModel, Depends()],
):
    # call GPTPrompter to reinforce automatically based on user's performance

    # mocking it here
    return mock_questions_list
