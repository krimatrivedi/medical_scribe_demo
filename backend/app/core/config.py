from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Medical Scribe AI"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./medical_scribe.db"
    GROQ_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
