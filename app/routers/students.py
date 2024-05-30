import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
        student: schemas.StudentBase = Body(..., alias='student'), db: Session = Depends(get_db)
) -> schemas.Student:
    return crud.create_student(db=db, student=student)


@router.get("/", response_model=List[schemas.Student], status_code=status.HTTP_200_OK)
def get_students(db: Session = Depends(get_db)) -> List[schemas.Student]:
    return crud.get_students(db=db)


@router.get("/{student_uuid}", response_model=schemas.Student)
def read_student(student_id: uuid.UUID, db: Session = Depends(get_db)) -> schemas.Student:
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.put("/{student_uuid}", response_model=schemas.Student, status_code=status.HTTP_200_OK)
def update_student(student_id: uuid.UUID, student: schemas.StudentBase, db: Session = Depends(get_db)) -> schemas.Student:
    return crud.update_student(db=db, student_id=student_id, student=student)


@router.patch("/{student_uuid}", response_model=schemas.Student, status_code=status.HTTP_200_OK)
def partial_update_student(
        student_id: uuid.UUID, student_data: schemas.PartialUpdateStudent, db: Session = Depends(get_db)
) -> schemas.Student:
    return crud.partial_update_student(db=db, student_id=student_id, student_fields=student_data)


@router.delete("/{student_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    crud.delete_student(db=db, student_id=student_id)
