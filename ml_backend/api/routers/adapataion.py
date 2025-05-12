from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ml_backend.api.models.schemas import AdaptationRequest, AdaptationResponse
from ml_backend.api.db.base import get_db
from ml_backend.api.services.adaptation_service import get_keywords_score

router = APIRouter()


@router.post("/adaptation", response_model=AdaptationResponse)
async def process_resume(request: AdaptationRequest, db: Session = Depends(get_db)):
    try:
        result = get_keywords_score(db, request.resume_id, request.vacancy_text)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
