from fastapi import FastAPI
from app.api.endpoints.doctor import router as doctor_router
from app.api.endpoints.welcome import router as welcome_router # import them with different names to avoid conflict
from app.api.endpoints.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:8081"
    "http://localhost:5173",
    "https://id-preview--02d2a22d-93ef-45ad-8b62-0622cfdaf956.lovable.app",
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(doctor_router)
app.include_router(welcome_router)
app.include_router(auth_router)











