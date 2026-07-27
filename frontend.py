"""
FastAPI wrapper around the existing Voicebot Doctor logic.

This exposes your speech-to-text, vision-diagnosis, and text-to-speech
pipeline as a JSON/multipart HTTP API, so a separately-hosted frontend
(e.g. built with Lovable) can call it directly instead of using the
Gradio UI.

Run locally with:
    uvicorn api:app --reload --port 8000

Endpoints:
    POST /diagnose
        multipart/form-data:
            audio: file  (patient's spoken symptoms)
            image: file  (medical image)
        returns: JSON diagnosis + base64-encoded spoken response audio
"""

import base64
import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.services.speech_to_text import transcribe_audio
from app.services.text_to_speech import speak_text
from app.clients.llm import ask_vision_model

load_dotenv()

app = FastAPI(title="Voicebot Doctor API")

# Allow your Lovable frontend (or any origin, while you're testing) to call this API.
# Once deployed, tighten this to your actual Lovable app URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/diagnose")
async def diagnose(audio: UploadFile = File(...), image: UploadFile = File(...)):
    # Save uploaded files to temp paths since the existing functions
    # expect file paths, not in-memory bytes.
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio.filename)[1]) as audio_tmp:
        audio_tmp.write(await audio.read())
        audio_path = audio_tmp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[1]) as image_tmp:
        image_tmp.write(await image.read())
        image_path = image_tmp.name

    try:
        # 1. Transcribe patient's spoken symptoms
        patient_query = transcribe_audio(audio_path)

        # 2. Get structured diagnosis from Gemini vision model
        medical_response = ask_vision_model(image_path, patient_query)

        # 3. Convert the spoken-friendly part of the response to audio
        response_audio_path = speak_text(medical_response.spoken_response)
        with open(response_audio_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        return {
            "patient_query": patient_query,
            "diagnosis": medical_response.model_dump(),
            "audio_response_base64": audio_base64,
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up temp files
        for path in (audio_path, image_path):
            if os.path.exists(path):
                os.remove(path)
