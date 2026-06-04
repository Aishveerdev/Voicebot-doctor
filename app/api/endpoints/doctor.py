
from fastapi import APIRouter, UploadFile, File , Depends
from app.models.schema import API_Response
from app.services import process_image_query
# from app.services.text_to_speech import speak_text
from app.services.jwt_verify import verify_token
from app.services.reports import get_report_history
from app.services.chat_orchestrator import orchestrate_chat

router = APIRouter()


@router.post("/analyze" ,response_model=API_Response)
async def analyze( user=Depends(verify_token) ,
                audio: UploadFile = File(...),
                image: UploadFile = File(...)
                ):

    return await orchestrate_chat(user, audio, image)



@router.get("/report-history")
async def get_report(user=Depends(verify_token)):
    return await get_report_history(user.id)