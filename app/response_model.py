from typing import List, Optional

from pydantic import BaseModel


class BinaryQuestion(BaseModel):
    difficulty: int
    desc: str
    choice_1: str
    choice_2: str


class GetQuestion(BaseModel):
    id: int
