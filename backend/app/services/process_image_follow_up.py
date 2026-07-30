from app.services.supabase_db import get_chat_session 
from app.services.reports import get_report_by_id , update_report
from app.models.prompt import build_image_followup_prompt
from app.services.llm import ask_vision_model
from app.services.supabase_db import save_message
from app.services.redis_func import add_message
from app.models.schema import API_Response
import logging
import os


logger = logging.getLogger(__name__)



async def image_follow_up ( user , image , patient_query , session_id):
    logger.info("image_follow_up started for user_id=%s session_id=%s", getattr(user, 'id', None), session_id)

    # get existing session  and report.
    session = await get_chat_session(session_id=session_id)
    report_id = session["report_id"]
    logger.info("Loaded chat session %s with report_id=%s", session_id, report_id)

    existing_report = await get_report_by_id(report_id=report_id)
    existing_medical_response = existing_report[0]["medical_response"]
    logger.info("Fetched existing report %s and medical response length=%d", report_id, len(existing_medical_response or ""))

    # save image temp
    image_path = f"temp_{image.filename}"
    with open(image_path, "wb") as f:
        f.write(await image.read())
    logger.info("Saved uploaded image to temporary path %s", image_path)

    # build prompt
    prompt = build_image_followup_prompt(existing_medical_response=existing_medical_response , patient_query=patient_query)
    logger.info("Built image follow-up prompt for session %s", session_id)

    # Use vision model
    ai_medical_response = await ask_vision_model(image_path=image_path , query=patient_query , prompt=prompt)
    logger.info("Vision model completed for session %s", session_id)

    # image count
    current_count = existing_report[0].get("image_count")

    if current_count is None:
     current_count = 0

    image_count = current_count + 1

    # update report with ai_medical_response
    await update_report (report_id=report_id , medical_response=ai_medical_response , image_count=image_count )
    logger.info("Updated report %s with new medical response", report_id)

    # save messages
    # In DB
    await save_message(session_id, role="user", content=patient_query)
    await save_message(session_id, role="assistant", content=ai_medical_response.description)
    logger.info("Saved user and assistant messages to DB for session %s", session_id)

    # In Redis
    await add_message(session_id, role="user", content=patient_query)
    await add_message(session_id, role="assistant",content=ai_medical_response.description)
    logger.info("Saved user and assistant messages to Redis for session %s", session_id)

    # Delete temp file
    
    try:
        os.remove(image_path)
        logger.debug("Deleted temp image file %s", image_path)
    except OSError as e:
            logger.error("Error occurred while deleting temp image file %s: %s", image_path, e)


    return API_Response( 
        patient_query=patient_query,
        diagnosis=ai_medical_response,
        session_id=session_id,
        report_id=report_id
    )




