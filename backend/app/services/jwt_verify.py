from fastapi import (HTTPException,Depends)
from fastapi.security import (HTTPBearer,HTTPAuthorizationCredentials)
from app.core.supabase_client import supabase
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials= Depends(security)):

    logger.info("verify_token started")

    token = credentials.credentials
    

    # Verifying token internally using supabase.
    try:

        logger.info(f"Token length: {len(token)}")

        response = supabase.auth.get_user(token)

        user = response.user

        logger.info(f"Authenticated user: {user.email}")

        return user

    except Exception as e:

        logger.error(f"Token verification FAILED: {str(e)}")

        raise HTTPException(

            status_code=401,

            detail="Invalid token"

        )