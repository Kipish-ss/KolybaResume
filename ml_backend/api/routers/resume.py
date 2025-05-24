from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ml_backend.api.models.schemas import ResumeRequest
from ml_backend.api.db.base import get_db
from ml_backend.api.services.resume_service import store_resume_vector
from ml_backend.api.db.models import Resume

router = APIRouter()


@router.put("/resume", status_code=status.HTTP_200_OK)
async def process_resume(request: ResumeRequest, db: Session = Depends(get_db)):
    resume = db.get(Resume, request.resume_id)
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {request.resume_id} not found"
        )
    store_resume_vector(db, resume)
    return {"status": "success", "message": "Resume vector updated successfully"}
