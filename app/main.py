from fastapi import FastAPI
from .database import engine, Base
from .routers import students, scores
from .core.logging import logger

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Создаем все таблицы при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Starting up the application")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")

app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(scores.router, prefix="/scores", tags=["scores"])
