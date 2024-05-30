from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()
