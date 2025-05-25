from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ml_backend.api.models.schemas import AdaptationRequest, AdaptationResponse
from ml_backend.api.db.base import get_db
from ml_backend.api.services.adaptation_service import get_keywords_score
from ml_backend.api.db.models import Resume
router = APIRouter()


@router.post("/adaptation", response_model=AdaptationResponse)
async def get_recommendations(request: AdaptationRequest, db: Session = Depends(get_db)):
    resume = db.get(Resume, request.resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {request.resume_id} not found"
        )
    if not request.vacancy_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vacancy text cannot be empty"
        )

    result = get_keywords_score(resume, request.vacancy_text, request.clean)

    return result
