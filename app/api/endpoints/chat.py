from fastapi import APIRouter, Depends
import logging
from app.models.schema import ChatRequest,ChatResponse , ChatMessageResponse
from app.services.chat_db import save_message, get_chat_history , get_chat_session
from app.services.chat_prompt import build_conversation, build_prompt
from app.services.jwt_verify import verify_token
from app.services.llm import ask_language_model
from app.services.reports import get_report_by_id


router = APIRouter(prefix="/chat",tags=["Chat"])

# Module logger
logger = logging.getLogger(__name__)

@router.post("/message", response_model=ChatResponse)
async def chat(
    session_id: str,
    request: ChatRequest,
    user=Depends(verify_token)
):
    # Log incoming request (avoid logging full user/token)
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
    await save_message(
        session_id,
        role="user",
        content=request.message)
    logger.debug("Saved user message for session %s", session_id)
    
    # Get chat history
    history = await get_chat_history(session_id)
    logger.debug("Fetched chat history for session %s (entries=%d)", session_id, len(history) if history is not None else 0)
    
    # Organize history into a prompt for the language model
    conversation = build_conversation(history)

# TO GET REPORT [medical_response] , WE NEED SESSION ID , THROUGH SESSION ID WE CAN GET REPORT ID AND THROUGH REPORT ID WE CAN GET REPORT DETAILS

    # Get session
    session = await get_chat_session(session_id)
    logger.debug("Fetched session for session_id=%s -> %s", session_id, getattr(session, 'id', None) if session else None)

    # Get report 
    report = await get_report_by_id(session["report_id"])  # we will provide medical diagnosis from  report to model for better context and better response
    logger.info("Fetched report for report_id=%s -> %s", session["report_id"], getattr(report, 'id', None) if report else None)
# NOW BUILD PROMPT WITH REPORT AND CONVERSATION HISTORY
    logger.info(f"Report object: {report}")
    logger.info(f"Report type: {type(report)}")
    prompt = build_prompt( medical_response =report[0]["medical_response"], conversation_history=conversation)
    logger.debug("Built prompt for LLM (prompt_len=%d)", len(prompt) if prompt else 0)

    
    # Get AI response
    try:
        ai_resposne = await ask_language_model(prompt)
    except Exception:
        logger.exception("LLM call failed for session %s", session_id)
        raise

    # Save assistant response
    await save_message(
        session_id,
        role="assistant",
        content=ai_resposne)
    logger.debug("Saved assistant response for session %s (response_len=%d)", session_id, len(ai_resposne) if ai_resposne else 0)

    logger.info("/chat/message completed for session %s", session_id)

    return ChatResponse(Response=ai_resposne)



@router.get("/history", response_model=list[ChatMessageResponse])
async def history(session_id: str, user=Depends(verify_token)):
    logger.info("/chat/history called: session_id=%s", session_id)
    history = await get_chat_history(session_id)
    logger.debug("Returning history entries=%d for session %s", len(history) if history is not None else 0, session_id)
    return history



@router.get("/test-gemini")
async def test_gemini():
    logger.info("/chat/test-gemini called")
    response = await ask_language_model(
        "Say hello"
    )
    logger.debug("Gemini test response length=%d", len(response) if response else 0)

    return {
        "response": response
    }