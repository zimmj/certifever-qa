from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db import db_models as m


class Repo:
    def __init__(self, db: Session):
        self._db = db

    def _add_entry(self, db_entry: m.Base):
        self._db.add(db_entry)
        self._db.commit()
        self._db.refresh(db_entry)
        return db_entry


class BinaryQuestionRepo(Repo):
    def __init__(self, db: Session):
        super().__init__(db)

    def create(
            self,
            difficulty: int,
            desc: str,
            choice_1: str,
            choice_2: str
    ) -> m.BinaryQuestion:

        db_question = m.BinaryQuestion(
            difficulty=difficulty,
            desc=desc,
            choice_1=choice_1,
            choice_2=choice_2
        )
        return self._add_entry(db_question)

    def get(
            self,
            question_id: int
    ) -> m.BinaryQuestion | None:
        return self._db.query(m.BinaryQuestion).filter(m.BinaryQuestion.id == question_id).first()
