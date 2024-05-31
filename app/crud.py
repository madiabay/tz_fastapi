from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import NoResultFound
from . import models, schemas
from fastapi import HTTPException, status

# STUDENTS
async def get_student(db: AsyncSession, student_id: UUID):
    try:
        result = await db.execute(
            select(models.Student).options(joinedload(models.Student.scores)).filter(models.Student.id == student_id)
        )
        return result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student not found")

async def get_students(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Student).options(joinedload(models.Student.scores)).offset(skip).limit(limit)
    )
    return result.unique().scalars().all()

async def create_student(db: AsyncSession, student: schemas.StudentBase):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student

async def update_student(db: AsyncSession, student_id: UUID, student: schemas.StudentBase):
    try:
        result = await db.execute(
            select(models.Student).filter(models.Student.id == student_id)
        )
        db_student = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student not found")

    db_student.name = student.name
    db_student.age = student.age
    await db.commit()
    await db.refresh(db_student)
    return db_student

async def partial_update_student(db: AsyncSession, student_id: UUID, student_fields: schemas.PartialUpdateStudent):
    try:
        result = await db.execute(
            select(models.Student).filter(models.Student.id == student_id)
        )
        db_student = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student not found")

    update_fields = student_fields.dict(exclude_unset=True)
    for k, v in update_fields.items():
        setattr(db_student, k, v)

    try:
        await db.commit()
        await db.refresh(db_student)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return db_student

async def delete_student(db: AsyncSession, student_id: UUID):
    try:
        result = await db.execute(
            select(models.Student).filter(models.Student.id == student_id)
        )
        db_student = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student not found with this ID")

    await db.delete(db_student)
    await db.commit()

# SCORES
async def get_score(db: AsyncSession, score_id: UUID):
    try:
        result = await db.execute(
            select(models.Score).filter(models.Score.id == score_id)
        )
        return result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Score not found")

async def get_scores(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Score).offset(skip).limit(limit)
    )
    return result.unique().scalars().all()

async def create_score(db: AsyncSession, score: schemas.ScoreBase):
    score_data = score.dict()
    try:
        result = await db.execute(
            select(models.Student).filter(models.Student.id == score_data['student_id'])
        )
        student = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Student with the specified ID was not found")

    db_score = models.Score(**score_data)
    db.add(db_score)
    await db.commit()
    await db.refresh(db_score)
    return db_score

async def update_score(db: AsyncSession, score_id: UUID, score: schemas.UpdateScore):
    try:
        result = await db.execute(
            select(models.Score).filter(models.Score.id == score_id)
        )
        db_score = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Score not found")

    db_score.score = score.score
    db_score.subject = score.subject
    await db.commit()
    await db.refresh(db_score)
    return db_score

async def partial_update_score(db: AsyncSession, score_id: UUID, score_fields: schemas.PartialUpdateScore):
    try:
        result = await db.execute(
            select(models.Score).filter(models.Score.id == score_id)
        )
        db_score = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Score not found")

    update_fields = score_fields.dict(exclude_unset=True)
    for k, v in update_fields.items():
        setattr(db_score, k, v)

    try:
        await db.commit()
        await db.refresh(db_score)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return db_score

async def delete_score(db: AsyncSession, score_id: UUID):
    try:
        result = await db.execute(
            select(models.Score).filter(models.Score.id == score_id)
        )
        db_score = result.unique().scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Score not found with this ID")

    await db.delete(db_score)
    await db.commit()
