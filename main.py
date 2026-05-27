import gradio as gr
import asyncio    
import logging
from models import Medical_Response , API_Response
from dotenv import load_dotenv
from speech_to_text import transcribe_audio
from text_to_speech import speak_text
from llm import ask_vision_model
from fastapi import FastAPI, UploadFile, File, Form


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    print("Received request to root endpoint")
    return {"message": "Welcome "}

@app.post("/analyze" ,response_model=API_Response)   
async def analyze(
        audio: UploadFile = File(...),
        image: UploadFile = File(...)):

    logger.info("Received /analyze request: audio=%s image=%s", audio.filename, image.filename)

    # SAVE AUDIO
    audio_path = f"temp_{audio.filename}"
    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    logger.debug("Saved audio file to %s", audio_path)

    # SAVE IMAGE
    image_path = f"temp_{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    logger.debug("Saved image file to %s", image_path)

    try:
        logger.info("Transcribing audio")
        patient_query = await transcribe_audio(audio_path)
        logger.info("Audio transcription complete")

        logger.info("Asking vision model")
        medical_response = await ask_vision_model(image_path, patient_query)
        logger.info("Vision model response received")

        logger.info("Generating spoken response")
        audio_response = speak_text(medical_response.spoken_response)
        logger.info("Text-to-speech conversion complete")

        return API_Response(
            patient_query=patient_query,
            diagnosis=medical_response,
            audio_response=audio_response
        )
    except Exception as e:
        logger.exception("Error processing /analyze request")
        return API_Response(
            patient_query="",
            diagnosis=Medical_Response(
                detected_issue="Unable to generate response",
                description="An unexpected error occurred while creating the medical response. Please try again.",
                severity="N/A",
                recommendations=["Please retry your request.", "If the problem persists, contact support."],
                should_consult_doctor=False,
                confidence=0.0,
                spoken_response="Sorry, I couldn't generate a response right now. Please try again."            ),
            audio_response=""
        )











