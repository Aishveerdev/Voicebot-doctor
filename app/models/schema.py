from pydantic import BaseModel
from typing import List
from datetime import datetime

class Medical_Response(BaseModel): 

    detected_issue: str
    description: str
    severity: str
    recommendations: List[str]
    should_consult_doctor: bool
    confidence: float 
   

class API_Response(BaseModel):
    patient_query: str
    diagnosis: Medical_Response
    session_id: str | None = None
    report_id: str | None = None


class ChatResponse(BaseModel):
    patient_query: str
    response: str              # plain text, no schema enforcement
    session_id: str | None = None
    report_id: str | None = None



class ChatMessageResponse ( BaseModel):
    role: str
    content: str

class SessionResponse(BaseModel):
    
    id: str
    user_id : str
    report_id: str | None = None
    created_at: datetime