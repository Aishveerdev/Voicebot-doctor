from pydantic import BaseModel
from typing import List

class Medical_Response(BaseModel): 

    detected_issue: str
    description: str
    severity: str
    recommendations: List[str]
    should_consult_doctor: bool
    confidence: float # for future analytics
    spoken_response: str # for text to speech conversion
