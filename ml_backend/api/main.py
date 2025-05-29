from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from ml_backend.api.routers import vacancies, resume, adapataion
from ml_backend.api.services.model_service import load_models
from ml_backend.api.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if settings.environment == "production":
    origins = ["https://kolybaresumebackend.onrender.com"]
else:
    origins = ["http://localhost", "http://127.0.0.1"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up: Loading ML models")
    load_models()
    logger.info("Models loaded successfully")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title="Resume Matching API",
    description="API for matching resumes with job vacancies",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(resume.router, tags=["Resume"])
app.include_router(vacancies.router, tags=["Vacancies"])
app.include_router(adapataion.router, tags=["Adaptation"])
