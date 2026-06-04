from fastapi import APIRouter, Depends
import logging
from app.models.schema import ChatRequest,ChatResponse , ChatMessageResponse
from app.services.process_text_querry import process_text_query
from app.services.supabase_db import get_chat_history
from app.services.jwt_verify import verify_token
from app.services.chat_orchestrator import orchestrate_chat


router = APIRouter(prefix="/chat",tags=["Chat"])

# Module logger
logger = logging.getLogger(__name__)

@router.post("/message", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest, user=Depends(verify_token)):
    return await orchestrate_chat(user, session_id=session_id, request=request)




@router.get("/history", response_model=list[ChatMessageResponse])
async def history(session_id: str, user=Depends(verify_token)):
    logger.info("/chat/history called: session_id=%s", session_id)
    history = await get_chat_history(session_id)
    logger.debug("Returning history entries=%d for session %s", len(history) if history is not None else 0, session_id)
    return history

