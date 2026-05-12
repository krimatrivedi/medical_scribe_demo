from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, transcribe, analyze, process_audio, patient, record, process_text
from app.core.config import settings
from app.core.logger import logger
from app.core.database import create_db_and_tables

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG
    )

    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(transcribe.router, tags=["Transcription"])
    app.include_router(analyze.router, tags=["Analysis"])
    app.include_router(process_audio.router, tags=["Process Audio"])
    app.include_router(patient.router, tags=["Patient"])
    app.include_router(record.router, tags=["Record"])
    app.include_router(process_text.router, tags=["Process Text"])

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up the Medical Scribe AI Backend...")
        create_db_and_tables()

    return app

app = create_app()
