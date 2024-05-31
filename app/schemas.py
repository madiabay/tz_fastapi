import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, validator


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
        from_attributes = True


class StudentBase(BaseModel):
    name: str
    age: int = Field(..., ge=0)

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Name must not be empty')
        return value

    class Config:
        from_attributes = True


class PartialUpdateStudent(StudentBase):
    name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)


class Student(StudentBase):
    id: uuid.UUID
    scores: List[ScoreBase] = []
