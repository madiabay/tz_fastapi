from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from typing import List
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Score, status_code=status.HTTP_201_CREATED)
def create_score(score: schemas.ScoreBase, db: Session = Depends(get_db)) -> schemas.Score:
    return crud.create_score(db=db, score=score)


@router.get("/", response_model=List[schemas.Score], status_code=status.HTTP_200_OK)
def get_scores(db: Session = Depends(get_db)) -> List[schemas.Score]:
    return crud.get_scores(db=db)


@router.get("/{score_uuid}", response_model=schemas.Score)
def read_score(score_id: uuid.UUID, db: Session = Depends(get_db)) -> schemas.Score:
    db_score = crud.get_score(db, score_id=score_id)
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return db_score


@router.put("/{score_uuid}", response_model=schemas.Score, status_code=status.HTTP_200_OK)
def update_score(score_id: uuid.UUID, score: schemas.UpdateScore, db: Session = Depends(get_db)) -> schemas.Score:
    return crud.update_score(db=db, score_id=score_id, score=score)


@router.patch("/{score_uuid}", response_model=schemas.Score, status_code=status.HTTP_200_OK)
def partial_update_score(
        score_id: uuid.UUID, score_data: schemas.PartialUpdateScore, db: Session = Depends(get_db)
) -> schemas.Score:
    return crud.partial_update_score(db=db, score_id=score_id, score_fields=score_data)


@router.delete("/{score_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_score(score_id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    crud.delete_score(db=db, score_id=score_id)
