import logging
import os
from fastapi import logger
from app.services.llm import ask_vision_model
from app.services.reports import create_report , update_report
from app.models.schema import API_Response, Medical_Response
from app.models.schema import Medical_Response
from app.services.supabase_db import update_chat_session




logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)

    

async def analyze_query(user,image=None , patient_query=None, session_id=None):
    
    logger.info(f"Current session id: {session_id} for user id: {user.id}")


    # SAVE IMAGE
    image_path = f"temp_{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    logger.debug("Saved image file to %s", image_path)

    try:
        logger.info("query received for image analysis, starting processing")


        # Create report.( processing )
        logger.info(f"creating report for user_id={user.id} with patient_query={patient_query}")
        report_id = await create_report(user.id, patient_query)

        #Update chat session with report id  
        logger.info(f"Updating chat session {session_id} with report_id={report_id}")
        await update_chat_session(session_id, report_id)
        logger.info(f"Chat session {session_id} updated with report_id={report_id}")

        logger.info("Asking vision model")
        medical_response = await ask_vision_model(image_path, patient_query)
        await update_report( report_id, medical_response)
        logger.info("Vision model response received")

        # Delete temp image file\
        try:
            os.remove(image_path)
            logger.debug("Deleted temp image file %s", image_path)
        except OSError as e:
            logger.error("Error occurred while deleting temp image file %s: %s", image_path, e)

        # logger.info("Generating spoken response")
        # audio_response = speak_text(medical_response.spoken_response)
        # logger.info("Text-to-speech conversion complete")

        return API_Response(
            report_id=report_id,
            session_id=session_id,
            patient_query=patient_query,
            diagnosis=medical_response
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
