import logging
from pathlib import Path
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware

from omegaconf import OmegaConf
from fastapi import FastAPI, Depends, HTTPException

from app.db.database import SessionLocal, engine, Base
import app.response_model as model
from app.db.crud import BinaryQuestionRepo
from gpt.chatpdf_api import any_api

logger = logging.getLogger(__name__)
server = FastAPI()

origins = ["*"]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



ENDPOINTS_FILE = Path(__file__).parent.resolve() / "endpoints.yaml"
ENDPOINTS = OmegaConf.load(ENDPOINTS_FILE)

key_path_pdf = "gpt/chatpdf_key.txt"
key_path = "gpt/api_key.txt"


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


def prepare_question_response(result):
    response = result["response"]

    l = []
    for r in response:
        print(r)
        q = model.Question(
            question=r["question"],
            options=r["options"],
            correct_answer_id=r["correct_answer_id"],
            explanation=r["explanation"],
            topic=r["topic"]
        )
        l.append(q)

    return model.QuestionsList(
        data=l
    )


@server.post(ENDPOINTS.create_questions_with_topic.path, response_model=model.QuestionsList)
def create_questions_with_topic(
        create_question_model: Annotated[model.CreateQuestionModelWithTopic, Depends()],
):
    profile = f"I am a {create_question_model.profile}. I want to learn for {create_question_model.intent}"
    # run question creator
    our_api = any_api()
    result = our_api.init_question(profile=profile, key_path=key_path)
    return prepare_question_response(result)


@server.post(ENDPOINTS.create_questions_with_pdf.path, response_model=model.QuestionsList)
def create_questions_with_pdf(
        create_question_model: Annotated[model.CreateQuestionModelWithPdf, Depends()],
):
    in_file = create_question_model.pdf_file
    file_location = f"{in_file.filename}"

    with open(file_location, "wb+") as file_object:
        file_object.write(in_file.file.read())

    profile = f"I am a {create_question_model.profile}. I want to {create_question_model.intent}"
    # run question creator
    our_api = any_api()
    result = our_api.init_question(profile=profile, pdf_path=file_location, key_path=key_path_pdf)

    return prepare_question_response(result)


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
