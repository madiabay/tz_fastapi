import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)

    scores = relationship("Score", back_populates="student")


class Score(Base):
    __tablename__ = 'scores'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    score = Column(Integer)
    subject = Column(String)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'))

    student = relationship("Student", back_populates="scores")
