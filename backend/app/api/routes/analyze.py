from fastapi import APIRouter, Depends, HTTPException
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import analysis_service, AnalysisService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_transcript(
    request: AnalysisRequest,
    service: AnalysisService = Depends(lambda: analysis_service)
):
    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")
    
    try:
        result = service.analyze_transcript(request.transcript)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
