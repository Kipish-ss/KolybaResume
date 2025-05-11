from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ml_backend.api.models.schemas import (
    VacanciesRequest,
    VacancyScoreResponse,
    ResumeVacancyMatch
)
from ml_backend.api.db.base import get_db
from ml_backend.api.services.vacancy_service import (
    store_vacancy_vectors,
    get_matches_for_resume
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/vacancies", response_model=list[VacancyScoreResponse])
async def process_vacancies(request: VacanciesRequest, db: Session = Depends(get_db)):
    try:
        if not request.vacancy_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No vacancy IDs provided"
            )
        results = store_vacancy_vectors(db, request.vacancy_ids)

        return results

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/vacancies/score/{resume_id}", response_model=list[ResumeVacancyMatch])
async def get_vacancy_matches(resume_id: int, db: Session = Depends(get_db)):
    try:
        matches = get_matches_for_resume(db, resume_id)

        if not matches:
            return []

        return matches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
