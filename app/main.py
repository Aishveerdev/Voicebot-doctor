from fastapi import FastAPI
from app.api.endpoints.doctor import router as doctor_router
from app.api.endpoints.welcome import router as welcome_router # import them with different names to avoid conflict
from app.api.endpoints.auth import router as auth_router



app = FastAPI()
app.include_router(doctor_router)
app.include_router(welcome_router)
app.include_router(auth_router)












