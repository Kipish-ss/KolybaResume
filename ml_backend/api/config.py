from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
