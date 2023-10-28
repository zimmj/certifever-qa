from sqlalchemy import Column, Integer, String, ForeignKey

from .database import Base


class BinaryQuestion(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    difficulty = Column(Integer, nullable=False)
    desc = Column(String, nullable=False)
    choice_1 = Column(String, nullable=False)   # the correct answer
    choice_2 = Column(String, nullable=False)
