import json
from app.services.analysis_service import analysis_service
from app.core.logger import logger

class ICDService:
    def __init__(self):
        self.dictionary = {
            "flu": "J10",
            "viral infection": "B34",
            "diabetes": "E11",
            "hypertension": "I10",
            "cough": "R05"
        }

    def suggest_icd_code(self, diagnosis: str) -> str:
        # Check dictionary
        clean_diagnosis = diagnosis.lower().strip()
        if clean_diagnosis in self.dictionary:
            return self.dictionary[clean_diagnosis]

        # LLM Fallback
        logger.info(f"ICD code not found for '{diagnosis}', querying LLM...")
        try:
            # We reuse the Groq client from analysis_service if possible, 
            # but for simplicity, calling the analysis_service's client directly
            if not analysis_service.client:
                return "unknown"

            prompt = f"Suggest the most relevant 3-digit ICD-10 code for: {diagnosis}. Respond ONLY with the code."
            completion = analysis_service.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"ICD LLM suggestion failed: {e}")
            return "unknown"

icd_service = ICDService()
