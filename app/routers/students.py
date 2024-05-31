import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
async def create_student(
        student: schemas.StudentBase = Body(..., alias='student'), db: AsyncSession = Depends(get_db)
) -> schemas.Student:
    return await crud.create_student(db=db, student=student)


@router.get("/", response_model=List[schemas.Student], status_code=status.HTTP_200_OK)
async def get_students(db: AsyncSession = Depends(get_db)) -> List[schemas.Student]:
    return await crud.get_students(db=db)


@router.get("/{student_id}", response_model=schemas.Student)
async def read_student(student_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> schemas.Student:
    db_student = await crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.put("/{student_id}", response_model=schemas.Student, status_code=status.HTTP_200_OK)
async def update_student(student_id: uuid.UUID, student: schemas.StudentBase, db: AsyncSession = Depends(get_db)) -> schemas.Student:
    return await crud.update_student(db=db, student_id=student_id, student=student)


@router.patch("/{student_id}", response_model=schemas.Student, status_code=status.HTTP_200_OK)
async def partial_update_student(
        student_id: uuid.UUID, student_data: schemas.PartialUpdateStudent, db: AsyncSession = Depends(get_db)
) -> schemas.Student:
    return await crud.partial_update_student(db=db, student_id=student_id, student_fields=student_data)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    await crud.delete_student(db=db, student_id=student_id)
