
from fastapi import APIRouter, Form, UploadFile, File , Depends, logger , HTTPException
from app.models.schema import API_Response
import logging
from app.services.jwt_verify import verify_token
from app.services.chat_orchestrator import orchestrate_chat
from app.models.schema import ChatMessageResponse , SessionResponse , ChatResponse
from app.services.supabase_db import get_chat_history , create_chat_session , get_all_sessions 
from app.services.reports import get_report_history
from typing import Union

router = APIRouter()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)





@router.post("/chat" ,response_model=Union[API_Response , ChatResponse])
async def chat( user=Depends(verify_token) ,
                session_id: str | None = Form(None) ,
                audio: UploadFile | None = File(None),
                text_query: str | None = Form(None),
                image: UploadFile | None = File(None)
                ):

    return await orchestrate_chat(user, audio, text_query, image, session_id=session_id)

@router.post("/create_session" , response_model=SessionResponse)
async def create_session ( user = Depends(verify_token)):
    return await create_chat_session ( user_id= user.id)

@router.get("/get_sessions" , response_model=list[SessionResponse])
async def get_all_sessions_of_user (user=Depends(verify_token)):
    return await get_all_sessions (user_id=user.id)


@router.get("/chat_history", response_model=list[ChatMessageResponse])
async def history(session_id: str, user=Depends(verify_token)):
    logger.info("/chat/history called: session_id=%s", session_id)
    history = await get_chat_history(session_id)
    logger.debug("Returning history entries=%d for session %s", len(history) if history is not None else 0, session_id)
    return history


# since each session can have only 1 report , we will retunbr all rpeorts attahced to user.
@router.get("/report-history")
async def get_report(user=Depends(verify_token)):
    return await get_report_history(user.id)