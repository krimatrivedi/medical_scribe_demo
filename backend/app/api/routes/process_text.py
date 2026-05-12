from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.services.analysis_service import analysis_service
from app.services.ner_service import ner_service
from app.services.icd_service import icd_service
from app.services.patient_service import patient_service
from app.core.database import get_session
from app.core.logger import logger
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class TextProcessRequest(BaseModel):
    patient_id: Optional[str] = None
    transcript: str

@router.post("/process-text")
async def process_text(
    request: TextProcessRequest,
    session: Session = Depends(get_session)
):
    try:
        logger.info(f"Processing text for patient: {request.patient_id}")
        
        # 1. Analysis (LLM)
        analysis = analysis_service.analyze_transcript(request.transcript)
        
        # 2. NER
        entities = ner_service.extract_entities(request.transcript)
        
        # 3. ICD Code
        icd_code = icd_service.suggest_icd_code(analysis.diagnosis)
        
        # 4. Save record if patient_id is provided
        if request.patient_id:
            patient_service.save_record(session, request.patient_id, request.transcript, analysis)
            logger.info(f"Record saved for patient: {request.patient_id}")

        return {
            "status": "success",
            "transcript": request.transcript,
            "structured_data": analysis,
            "entities": entities,
            "icd_code": icd_code,
            "error": None
        }

    except Exception as e:
        logger.error(f"Text pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
