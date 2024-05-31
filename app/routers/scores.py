from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Score, status_code=status.HTTP_201_CREATED)
async def create_score(score: schemas.ScoreBase, db: AsyncSession = Depends(get_db)) -> schemas.Score:
    return await crud.create_score(db=db, score=score)


@router.get("/", response_model=List[schemas.Score], status_code=status.HTTP_200_OK)
async def get_scores(db: AsyncSession = Depends(get_db)) -> List[schemas.Score]:
    return await crud.get_scores(db=db)


@router.get("/{score_id}", response_model=schemas.Score)
async def read_score(score_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> schemas.Score:
    db_score = await crud.get_score(db, score_id=score_id)
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return db_score


@router.put("/{score_id}", response_model=schemas.Score, status_code=status.HTTP_200_OK)
async def update_score(score_id: uuid.UUID, score: schemas.UpdateScore, db: AsyncSession = Depends(get_db)) -> schemas.Score:
    return await crud.update_score(db=db, score_id=score_id, score=score)


@router.patch("/{score_id}", response_model=schemas.Score, status_code=status.HTTP_200_OK)
async def partial_update_score(
        score_id: uuid.UUID, score_data: schemas.PartialUpdateScore, db: AsyncSession = Depends(get_db)
) -> schemas.Score:
    return await crud.partial_update_score(db=db, score_id=score_id, score_fields=score_data)


@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_score(score_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    await crud.delete_score(db=db, score_id=score_id)
