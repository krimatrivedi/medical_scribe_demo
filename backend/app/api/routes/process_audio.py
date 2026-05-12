import os
import shutil
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlmodel import Session
from app.services.transcription_service import transcription_service
from app.services.analysis_service import analysis_service
from app.services.patient_service import patient_service
from app.services.icd_service import icd_service
from app.core.database import get_session
from app.core.logger import logger

router = APIRouter()

@router.post("/process-audio")
async def process_audio(
    file: UploadFile = File(...),
    patient_id: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    temp_file_path = f"temp_{file.filename}"
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        transcript = transcription_service.transcribe(temp_file_path)

        if not transcript:
            return {"status": "no_speech_detected", "transcript": "", "structured_data": None, "error": None}

        analysis = analysis_service.analyze_transcript(transcript)

        icd_code = icd_service.suggest_icd_code(analysis.diagnosis)

        analysis.icd_code = icd_code
        
        # Always save record for correction support
        p_id = patient_id if patient_id else "anonymous_patient"
        record = patient_service.save_record(session, p_id, transcript, analysis)
        logger.info(f"Record saved with ID: {record.id}")

        return {
            "status": "success",
            "transcript": transcript,
            "structured_data": analysis,
            "icd_code": icd_code,
            "record_id": record.id,
            "error": None
        }

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        return {
            "status": "partial_success" if 'transcript' in locals() else "error",
            "transcript": transcript if 'transcript' in locals() else None,
            "structured_data": None,
            "error": str(e)
        }
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
