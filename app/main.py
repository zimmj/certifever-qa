import json
import logging
from pathlib import Path
from typing import Annotated
from flask import Flask, jsonify
from fastapi import Depends, APIRouter, Response

from omegaconf import OmegaConf
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import JSONResponse

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


@server.post(ENDPOINTS.create_bin_question.path)
def create_binary_question(
    bin_question: Annotated[model.BinaryQuestion, Depends()],
    bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):
    logging.info("Creating question")

    # WARNING: we are not checking if there's duplicate now
    bin_question = bin_question_repo.create(
        topic=bin_question.topic,
        difficulty=bin_question.difficulty,
        question=bin_question.question,
        correct_answer=bin_question.correct_answer,
        explanation=bin_question.explanation,
        example=bin_question.example
    )

    return {"message": f"BinaryQuestion created successfully, id = {bin_question.id}"}
@server.get(ENDPOINTS.get_bin_questions.path, response_model=model.BinaryQuestions)
def get_bin_questions(
    get_bin_question_list: Annotated[model.GetBinaryQuestionsByTopicAndDifficulty, Depends()],
    bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):
    questions = bin_question_repo.getBinaryQuestionsByTopicAndDifficulty(get_bin_question_list.topic
                                                                         , get_bin_question_list.difficulty)
    modelQL = []
    for q in questions:
        entry = model.BinaryQuestion(
            topic=q.topic,
            difficulty=q.difficulty,
            question=q.question,
            correct_answer=q.correct_answer,
            explanation=q.explanation,
            example=q.example
        )
        modelQL.append(entry)

    return model.BinaryQuestions(data=modelQL)

@server.post(ENDPOINTS.create_bin_quiz_by_uploading_file.path, response_model=model.TopicName)
def create_bin_quiz_by_uploading_file(
        upload_file: Annotated[model.UploadFile, Depends()],
        bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):

    return model.TopicName(topic="upload_file_name")

@server.get(ENDPOINTS.get_bin_question.path, response_model=model.BinaryQuestion)
def get_bin_question(
        get_bin_question_model: Annotated[model.GetQuestion, Depends()],
        bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):
    logging.info(f"Getting question of id {get_bin_question_model.id}")

    q = bin_question_repo.get(get_bin_question_model.id)
    if q is None:
        logging.error(f"BinaryQuestion of id {get_bin_question_model.id} not found")
        raise HTTPException(status_code=404, detail="BinaryQuestion not found")

    return model.BinaryQuestion(
        topic=q.topic,
        difficulty=q.difficulty,
        question=q.question,
        correct_answer=q.correct_answer,
        explanation=q.explanation,
        example=q.example
    )
