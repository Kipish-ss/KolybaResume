from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import nltk
from ml_backend.api.routers import vacancies, resume, adapataion
from ml_backend.api.services.model_service import load_models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up: Loading ML models")
    load_models()
    logger.info("Models loaded successfully")

    nltk.download('stopwords')
    logger.info("Stopwords downloaded successfully")

    yield

    logger.info("Application shutting down")


app = FastAPI(
    title="Resume Matching API",
    description="API for matching resumes with job vacancies",
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, tags=["Resume"])
app.include_router(vacancies.router, tags=["Vacancies"])
app.include_router(adapataion.router, tags=["Adaptation"])
