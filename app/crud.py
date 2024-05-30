from uuid import UUID
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status


# STUDENTS
def get_student(db: Session, student_id: UUID):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: schemas.StudentBase):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: UUID, student: schemas.StudentBase):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.age = student.age
    db.commit()
    db.refresh(db_student)
    return db_student


def partial_update_student(db: Session, student_id: UUID, student_fields: schemas.PartialUpdateStudent):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_fields = student_fields.dict(exclude_defaults=True)
    for k, v in update_fields.items():
        setattr(db_student, k, v)

    try:
        db.commit()
        db.refresh(db_student)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return db_student


def delete_student(db: Session, student_id: UUID):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found with this ID")

    db.delete(db_student)
    db.commit()


# SCORES
def get_score(db: Session, score_id: UUID):
    return db.query(models.Score).filter(models.Score.id == score_id).first()


def get_scores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Score).offset(skip).limit(limit).all()


def create_score(db: Session, score: schemas.ScoreBase):
    score_data = score.dict()
    student = db.query(models.Student).filter(models.Student.id == score_data['student_id']).first()
    if not student:
        raise HTTPException(status_code=404, detail="User with the specified ID was not found")

    db_score = models.Score(**score_data)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def update_score(db: Session, score_id: UUID, score: schemas.UpdateScore):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")

    db_score.score = score.score
    db_score.subject = score.subject
    db.commit()
    db.refresh(db_score)
    return db_score


def partial_update_score(db: Session, score_id: UUID, score_fields: schemas.PartialUpdateScore):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found")

    update_fields = score_fields.dict(exclude_defaults=True)
    for k, v in update_fields.items():
        setattr(db_score, k, v)

    try:
        db.commit()
        db.refresh(db_score)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return db_score


def delete_score(db: Session, score_id: UUID):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not db_score:
        raise HTTPException(status_code=404, detail="Score not found with this ID")

    db.delete(db_score)
    db.commit()
