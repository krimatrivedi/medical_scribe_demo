import sys
import os

# Add the current directory to sys.path so 'app' can be found
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from app.main import create_app
import json

app = create_app()
client = TestClient(app)

def test_analyze():
    payload = {
        "transcript": "Patient reports fever, headache and mild cough for 3 days. Doctor suspects viral infection and prescribes paracetamol."
    }
    
    print(f"Sending request to /analyze with payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = client.post("/analyze", json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response JSON:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred during the request: {e}")

if __name__ == "__main__":
    test_analyze()
