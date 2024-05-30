import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from . import constants


class ScoreBase(BaseModel):
    score: int = Field(..., ge=0, le=10)
    subject: str
    student_id: uuid.UUID


class UpdateScore(BaseModel):
    score: int = Field(..., ge=0, le=10)
    subject: str


class PartialUpdateScore(BaseModel):
    score: Optional[int] = Field(None, ge=0, le=10)
    subject: Optional[str] = None


class Score(ScoreBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    age: int = Field(..., ge=0)


class PartialUpdateStudent(StudentBase):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=10)

    class Config:
        orm_mode = True


class Student(StudentBase):
    id: uuid.UUID
    scores: List[ScoreBase] = []

    class Config:
        orm_mode = True
