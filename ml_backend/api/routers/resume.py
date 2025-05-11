from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ml_backend.api.models.schemas import ResumeRequest
from ml_backend.api.db.base import get_db
from ml_backend.api.services.resume_service import store_resume_vector

router = APIRouter()


@router.put("/resume", status_code=status.HTTP_200_OK)
async def process_resume(request: ResumeRequest, db: Session = Depends(get_db)):
    try:
        store_resume_vector(db, request.resume_id)
        return {"status": "success", "message": "Resume Vector updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
