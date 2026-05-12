from transformers import pipeline
from app.core.logger import logger

class NERService:
    def __init__(self):
        logger.info("Loading Biomedical NER model...")
        # Using a smaller model for efficiency
        self.pipe = pipeline("token-classification", model="d4data/biomedical-ner-all", aggregation_strategy="simple")
        logger.info("NER model loaded.")

    def extract_entities(self, text: str) -> dict:
        results = self.pipe(text)
        
        entities = {
            "symptoms": set(),
            "diseases": set(),
            "medications": set()
        }

        # Mapping model labels to our schema
        label_map = {
            "Sign_Symptoms": "symptoms",
            "Disease": "diseases",
            "Drug": "medications"
        }

        for entity in results:
            label = entity['entity_group']
            word = entity['word'].strip()
            
            if label in label_map:
                entities[label_map[label]].add(word)

        return {
            "symptoms": list(entities["symptoms"]),
            "diseases": list(entities["diseases"]),
            "medications": list(entities["medications"])
        }

ner_service = NERService()
