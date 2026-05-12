from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.correction_service import correction_service, CorrectionUpdate

router = APIRouter()

@router.get("/record/{record_id}")
async def get_record(record_id: int, session: Session = Depends(get_session)):
    record = correction_service.get_record(session, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "original": {
            "symptoms": record.symptoms,
            "diagnosis": record.diagnosis,
            "medications": record.medications,
            "notes": record.notes
        },
        "corrected": {
            "symptoms": record.corrected_symptoms,
            "diagnosis": record.corrected_diagnosis,
            "medications": record.corrected_medications,
            "notes": record.corrected_notes
        } if record.is_corrected else None
    }

@router.put("/record/{record_id}/correct")
async def correct_record(record_id: int, update: CorrectionUpdate, session: Session = Depends(get_session)):
    record = correction_service.update_correction(session, record_id, update)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
