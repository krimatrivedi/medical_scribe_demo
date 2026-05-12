from sqlmodel import Session
from app.models.patient_record import PatientRecord
from pydantic import BaseModel
from typing import List, Optional

class CorrectionUpdate(BaseModel):
    symptoms: List[str]
    diagnosis: str
    medications: List[str]
    notes: Optional[str] = None

class CorrectionService:
    def get_record(self, session: Session, record_id: int) -> Optional[PatientRecord]:
        return session.get(PatientRecord, record_id)

    def update_correction(self, session: Session, record_id: int, update: CorrectionUpdate) -> Optional[PatientRecord]:
        record = self.get_record(session, record_id)
        if not record:
            return None
        
        record.corrected_symptoms = update.symptoms
        record.corrected_diagnosis = update.diagnosis
        record.corrected_medications = update.medications
        record.corrected_notes = update.notes
        record.is_corrected = True
        
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

correction_service = CorrectionService()
