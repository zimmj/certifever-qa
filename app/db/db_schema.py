from sqlalchemy import Column, Integer, String, ForeignKey

from .database import Base


class BinaryQuestion(Base):
    __tablename__ = 'questions_binary'
    id = Column(Integer, primary_key=True)
    topic = Column(String,nullable=False)
    difficulty = Column(Integer, nullable=False)
    question = Column(String, nullable=False)
    correct_answer = Column(Integer, nullable=False)
    explanation = Column(String, nullable=True)

class MultipleChoiceQuestion(Base):
    __tablename__ = 'questions_mutliplechoice'
    id = Column(Integer, primary_key=True)
    topic = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    question = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    wrong_answer1= Column(String, nullable=False)
    wrong_answer2 = Column(String, nullable=False)
    wrong_answer3 = Column(String, nullable=False)
    explanation = Column(String, nullable=True)
