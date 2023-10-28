import logging
from pathlib import Path

from omegaconf import OmegaConf
from fastapi import FastAPI

from app.db.database import SessionLocal, engine, Base

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


@server.on_event("startup")
async def startup_event():
    # Create the database tables
    Base.metadata.create_all(bind=engine)


@server.get(ENDPOINTS.root.path)
def root():
    return {"message": "AI Prompter Server is running"}
