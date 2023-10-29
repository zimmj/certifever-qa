from sqlalchemy.orm import Session

from app.db import db_schema as schema
from typing import List

class Repo:
    def __init__(self, db: Session):
        self._db = db

    def _add_entry(self, db_entry: schema.Base):
        self._db.add(db_entry)
        self._db.commit()
        self._db.refresh(db_entry)
        return db_entry


class BinaryQuestionRepo(Repo):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(
            self,
            topic: str,
            difficulty: int,
            question: str,
            correct_answer: int,
            explanation: str,
            example: str
    ) -> schema.BinaryQuestion:

        db_question = schema.BinaryQuestion(
            topic=topic,
            difficulty=difficulty,
            question=question,
            correct_answer=correct_answer,
            explanation=explanation,
            example=example
        )
        return self._add_entry(db_question)

    def getBinaryQuestionsByTopicAndDifficulty(
            self
            , topic: str
            , difficulty: int) -> List[schema.BinaryQuestion]:
        questions = self._db.query(schema.BinaryQuestion)\
            .filter(schema.BinaryQuestion.topic == topic)\
            .filter(schema.BinaryQuestion.difficulty == difficulty)\
            .all()
        return questions if questions else []  # Returning a list or an empty list if no questions found
    def get(
            self,
            question_id: int
    ) -> schema.BinaryQuestion | None:
        return self._db.query(schema.BinaryQuestion).filter(schema.BinaryQuestion.id == question_id).first()
