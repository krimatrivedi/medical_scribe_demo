from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import shutil
import os
import tempfile
from app.services.transcription_service import transcription_service, TranscriptionService
from app.core.logger import logger

router = APIRouter()

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    service: TranscriptionService = Depends(lambda: transcription_service)
):
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Validate file size (approximate check using SpooledTemporaryFile if available)
    # For more robust checks, we'd check content-length or read in chunks
    
    try:
        # Create a temporary file to store the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name

        # Verify file size of the saved temp file
        if os.path.getsize(tmp_path) > MAX_FILE_SIZE:
            os.remove(tmp_path)
            raise HTTPException(status_code=413, detail="File too large. Max size is 25MB.")

        # Transcribe
        transcript = service.transcribe(tmp_path)

        # Cleanup
        os.remove(tmp_path)

        return {"transcript": transcript}

    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise HTTPException(status_code=500, detail="Transcription failed.")
