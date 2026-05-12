from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    transcript: str

class AnalysisResponse(BaseModel):
    symptoms: List[str]
    diagnosis: str
    medications: List[str]
    notes: Optional[str] = ""
    icd_code: Optional[str] = None 
