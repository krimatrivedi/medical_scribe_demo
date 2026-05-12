from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.patient_service import patient_service

router = APIRouter()

@router.get("/patient/{patient_id}/history")
async def get_patient_history(patient_id: str, session: Session = Depends(get_session)):
    history = patient_service.get_patient_history(session, patient_id)
    return [
        {
            "id": r.id,
            "date": r.created_at,
            "diagnosis": r.diagnosis,
            "symptoms": r.symptoms
        } for r in history
    ]
