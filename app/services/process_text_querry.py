import logging
from app.services.llm import ask_language_model
from app.services.reports import get_report_by_id
from app.services.redis_memory import get_chat_context
from app.services.redis_func import add_message
from app.services.supabase_db import save_message, get_chat_history , get_chat_session
from app.models.prompt import build_conversation, build_prompt
from app.models.schema import ChatRequest,ChatResponse , ChatMessageResponse



logger = logging.getLogger(__name__)








async def process_text_query(user , session_id, request):
    logger.info("process_text_query called for session_id=%s user_id=%s message_len=%d",
                session_id, getattr(user, 'id', None), len(request.message) if request and getattr(request, 'message', None) else 0)
    try:
        user_id = None
        if isinstance(user, dict):
            user_id = user.get("id") or user.get("user_id")
        else:
            user_id = getattr(user, "id", None)
    except Exception:
        user_id = None

    logger.info("/chat/message called: session_id=%s user_id=%s message_len=%d",
                session_id, user_id, len(request.message) if request and getattr(request, 'message', None) else 0)

    # Save user message

    # In DB
    await save_message(
        session_id,
        role="user",
        content=request.message)
    logger.debug("Saved user message in DB for session %s", session_id)

    # In Redis
    await add_message(
        session_id,
        role="user",
        content=request.message)
    logger.debug("Saved user message in Redis for session %s", session_id)


    # Get chat history from Redis or DB
    history = await get_chat_context(session_id)
    logger.debug("Fetched chat history for session %s (entries=%d)", session_id, len(history) if history is not None else 0)
    
    # Organize history into a prompt for the language model
    conversation_history = build_conversation(history)

# TO GET REPORT [medical_response] , WE NEED SESSION ID , THROUGH SESSION ID WE CAN GET REPORT ID AND THROUGH REPORT ID WE CAN GET REPORT DETAILS
# Since session is the root and we updated it with report id later in process_image_query, so we can easily get report id through session and then we can get report details through report id.

    # Get session
    session = await get_chat_session(session_id)
    logger.debug("Fetched session for session_id=%s -> %s", session_id, getattr(session, 'id', None) if session else None)

    # Get report 
    report = await get_report_by_id(session["report_id"])  # we will provide medical diagnosis from  report to model for better context and better response
    logger.info("Fetched report for report_id=%s -> %s", session["report_id"], "found" if report else "not found")
# NOW BUILD PROMPT WITH REPORT AND CONVERSATION HISTORY

    prompt = build_prompt( medical_response =report[0]["medical_response"], conversation_history=conversation_history)
    logger.debug("Built prompt for LLM (prompt_len=%d)", len(prompt) if prompt else 0)

    
    # Get AI response
    try:
        ai_resposne = await ask_language_model(prompt)
    except Exception:
        logger.exception("LLM call failed for session %s", session_id)
        raise

    # Save assistant response

    # In DB
    await save_message(
        session_id,
        role="assistant",
        content=ai_resposne)
    logger.debug("Saved assistant responsein DB for session %s (response_len=%d)", session_id, len(ai_resposne) if ai_resposne else 0)

    # In redis
    await add_message(
        session_id,
        role="assistant",
        content=ai_resposne)
    logger.info("Saved assistant response in Redis for session %s", session_id)


    logger.info("/chat/message completed for session %s", session_id)

    return ChatResponse(Response=ai_resposne)

