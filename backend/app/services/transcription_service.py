import whisper
import os
from app.core.logger import logger

class TranscriptionService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranscriptionService, cls).__new__(cls)
        return cls._instance

    def _load_model(self):
        if self._model is None:
            logger.info("Loading Whisper 'tiny' model...")
            self._model = whisper.load_model("tiny")
            logger.info("Whisper model loaded successfully.")

    def transcribe(self, file_path: str) -> str:
        self._load_model()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at {file_path}")
        
        logger.info(f"Starting transcription for {file_path}...")
        result = self._model.transcribe(file_path)
        return result.get("text", "").strip()

transcription_service = TranscriptionService()
