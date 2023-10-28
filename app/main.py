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


@server.post(ENDPOINTS.create_bin_question.path)
def create_binary_question(
    bin_question: Annotated[model.BinaryQuestion, Depends()],
    bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):
    logging.info("Creating question")

    # WARNING: we are not checking if there's duplicate now
    bin_question = bin_question_repo.create(
        difficulty=bin_question.difficulty,
        desc=bin_question.desc,
        choice_1=bin_question.choice_1,
        choice_2=bin_question.choice_2
    )

    return {"message": f"BinaryQuestion created successfully, id = {bin_question.id}"}


@server.get(ENDPOINTS.get_bin_question.path, response_model=model.BinaryQuestion)
def get_bin_question(
        get_bin_question_model: Annotated[model.GetQuestion, Depends()],
        bin_question_repo: Annotated[BinaryQuestionRepo, Depends(get_binary_question_repo)]
):
    logging.info(f"Getting question of id {get_bin_question_model.id}")

    question = bin_question_repo.get(get_bin_question_model.id)
    if question is None:
        logging.error(f"BinaryQuestion of id {get_bin_question_model.id} not found")
        raise HTTPException(status_code=404, detail="BinaryQuestion not found")

    return model.BinaryQuestion(
        difficulty=question.difficulty,
        desc=question.desc,
        choice_1=question.choice_1,
        choice_2=question.choice_2
    )