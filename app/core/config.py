from pydantic import BaseSettings


class Settings(BaseSettings):
PROJECT_NAME: str = "Auth Service"
DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/authdb"
JWT_SECRET: str = "CHANGE_ME_TO_A_STRONG_SECRET"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
REFRESH_TOKEN_EXPIRE_DAYS: int = 30
ALGORITHM: str = "HS256"


class Config:
env_file = ".env"


settings = Settings()