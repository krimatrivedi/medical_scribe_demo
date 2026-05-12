# Medical Scribe AI 🩺🎙️

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Groq](https://img.shields.io/badge/Groq-Llama--3-orange?style=for-the-badge)](https://groq.com/)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-blue?style=for-the-badge)](https://github.com/openai/whisper)

**Medical Scribe AI** is a state-of-the-art clinical documentation assistant designed to streamline the medical consultation process. By leveraging advanced speech-to-text (OpenAI Whisper) and Large Language Models (LLM), it transforms patient-doctor conversations into structured, actionable medical records in real-time.

---

## 🚀 Key Features

- **Real-time Transcription:** High-fidelity audio transcription using OpenAI Whisper.
- **AI-Powered Analysis:** Automatic extraction of symptoms, diagnosis, and medications using Llama-3 (via Groq).
- **ICD-10 Integration:** Intelligent suggestion of ICD-10 diagnostic codes based on clinical findings.
- **Patient Management:** Comprehensive system to track patient history and clinical records.
- **Correction Support:** Feedback loop to refine and correct AI-generated insights.
- **Seamless UI:** Modern, intuitive React-based frontend for healthcare professionals.

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Database:** SQLModel (SQLAlchemy + Pydantic)
- **AI/ML:** 
  - **Transcription:** OpenAI Whisper
  - **Inference Engine:** Groq (Llama-3-70b)
- **Validation:** Pydantic V2

### Frontend
- **Framework:** React 19
- **Bundler:** Vite
- **HTTP Client:** Axios
- **Styling:** CSS (Modern Responsive Design)

---

## 🏗️ Architecture

1.  **Audio Capture:** The frontend captures clinical audio and sends it to the FastAPI backend.
2.  **Transcription Pipeline:** The backend processes audio through OpenAI Whisper to generate a high-accuracy transcript.
3.  **NLP Analysis:** The transcript is analyzed by Llama-3 to identify key clinical entities (NER) and structure the data.
4.  **Diagnostic Coding:** The system suggests relevant ICD-10 codes based on the structured diagnosis.
5.  **Data Persistence:** Records are saved to the database for future reference and longitudinal patient care.

---

## 🚦 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm
- [Groq API Key](https://console.groq.com/)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   # Add your GROQ_API_KEY and DATABASE_URL
   ```
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## 📽️ Demo

Check out the product demo: `medical_scrtibe.mp4`

---

## 🛡️ Security & Privacy
This application is a prototype. In a production environment, ensure:
- Full HIPAA compliance for data handling.
- End-to-end encryption for audio and patient data.
- Secure authentication and authorization (e.g., OAuth2/OpenID Connect).

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

---
*Created with ❤️ for the healthcare community.*
