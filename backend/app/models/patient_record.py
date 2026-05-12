from typing import List, Optional
from sqlmodel import SQLModel, Field, JSON, Column
from datetime import datetime

class PatientRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: str = Field(index=True)
    transcript: str
    symptoms: List[str] = Field(sa_column=Column(JSON))
    diagnosis: str
    medications: List[str] = Field(sa_column=Column(JSON))
    notes: Optional[str] = None
    corrected_symptoms: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    corrected_diagnosis: Optional[str] = None
    corrected_medications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    corrected_notes: Optional[str] = None
    is_corrected: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
