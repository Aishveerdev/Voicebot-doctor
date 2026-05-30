import logging
from fastapi import logger
from app.services.llm import ask_vision_model
from app.services.speech_to_text import transcribe_audio
from app.services.reports import create_report , update_report
from app.models.schema import API_Response, Medical_Response
from app.models.schema import Medical_Response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)

    

async def analyze_query(user, audio, image):
    
    logger.info(f"Current user id: {user.id}")

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
        logger.info(f"creating report for user_id={user.id} with patient_query={patient_query}")
        report_id = await create_report(user.id, patient_query)
        # We returned report_id in cretae report function thats why now we can store it in variable " report id " is create report function's outpu t,, spo we are basicallty storing output of create report function which is nothing but report id.

        logger.info("Asking vision model")
        medical_response = await ask_vision_model(image_path, patient_query)
        await update_report( report_id, medical_response)
        logger.info("Vision model response received")

        # logger.info("Generating spoken response")
        # audio_response = speak_text(medical_response.spoken_response)
        # logger.info("Text-to-speech conversion complete")

        return API_Response(
            patient_query=patient_query,
            diagnosis=medical_response,
            # audio_response=audio_response
        )
    # TEXT TO SPEECH WOUL DBE HANDLED IN FRONTEND ONLY. 

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
                spoken_response="Sorry, I couldn't generate a response right now. Please try again."),
            audio_response=""
        )
