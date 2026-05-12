from typing import List
from sqlmodel import Session, select
from app.models.patient_record import PatientRecord
from app.schemas.analysis import AnalysisResponse

class PatientService:
    def save_record(self, session: Session, patient_id: str, transcript: str, analysis: AnalysisResponse) -> PatientRecord:
        record = PatientRecord(
            patient_id=patient_id,
            transcript=transcript,
            symptoms=analysis.symptoms,
            diagnosis=analysis.diagnosis,
            medications=analysis.medications,
            notes=analysis.notes
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

    def get_patient_history(self, session: Session, patient_id: str) -> List[PatientRecord]:
        statement = select(PatientRecord).where(PatientRecord.patient_id == patient_id).order_by(PatientRecord.created_at.desc())
        results = session.exec(statement).all()
        return list(results)

patient_service = PatientService()
