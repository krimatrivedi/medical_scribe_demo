import json
from groq import Groq
from app.core.config import settings
from app.core.logger import logger
from app.schemas.analysis import AnalysisResponse

class AnalysisService:
    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        else:
            logger.warning("GROQ_API_KEY not found in settings. Analysis service will be unavailable.")

    def analyze_transcript(self, transcript: str) -> AnalysisResponse:
        if not self.client:
            raise ValueError("Groq client not initialized. Check GROQ_API_KEY.")

        system_prompt = (
            "You are a medical assistant. Extract structured clinical information from conversations. "
            "Respond ONLY with a valid JSON object containing: "
            "symptoms (list of strings), diagnosis (string), medications (list of strings), and notes (string summary)."
        )

        user_prompt = f"Transcript: {transcript}\n\nProvide the structured JSON output:"

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
            )

            response_data = json.loads(completion.choices[0].message.content)
            
            # Validate and return using Pydantic
            return AnalysisResponse(**response_data)

        except Exception as e:
            logger.error(f"Groq analysis error: {str(e)}")
            # Fallback/Default response in case of error
            return AnalysisResponse(
                symptoms=[],
                diagnosis="Analysis failed",
                medications=[],
                notes=f"Error: {str(e)}"
            )

analysis_service = AnalysisService()
