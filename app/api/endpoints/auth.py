import logging
from fastapi import APIRouter
from app.core.supabase_client import supabase
from pydantic import EmailStr



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth" , tags=["Auth"])

@router.post("/signup")
async def signup(email: EmailStr, password: str):
    try:
        logger.info(f"Signup attempt for email: {email}")
        user = supabase.auth.sign_up({'email': email, 'password': password})
        logger.info(f"Suprabase response: {user}")
        logger.info(f"Signup successful for: {email}")
        return {"message": "User signed up successfully", "user": user}
    except Exception as e:
        logger.info(f"Signup failed: {str(e)}")
        return {"error": str(e)}
    

@router.post("/login")
async def login(email: EmailStr, password: str):
    try: 
        logger.info(f"Login attempt for email: {email}")

        user = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        logger.info(f"Login successful for: {email}")

        return {"message": "User logged in successfully", "user": user}
    except Exception as e:
        logger.info(f"Login failed: {str(e)}")
        return {"error": str(e)}