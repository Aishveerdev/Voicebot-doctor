from fastapi import FastAPI
from app.api.endpoints.doctor import router as doctor_router
from app.api.endpoints.welcome import router as welcome_router # import them with different names to avoid conflict
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.chat import router as chat_router



app = FastAPI()
app.include_router(doctor_router)
app.include_router(welcome_router)
app.include_router(auth_router)
app.include_router(chat_router)











