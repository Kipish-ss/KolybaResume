from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/kolybaresumedb"
    )

    API_PREFIX: str = "/api"

    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml_backend/resume_classifier/fine_tuned_bert")

    class Config:
        env_file = ".env"


settings = Settings()
