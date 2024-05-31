from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()
