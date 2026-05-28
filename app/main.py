from fastapi import FastAPI
from app.api.endpoints.doctor import router as doctor_router
from app.api.endpoints.welcome import router as welcome_router
# because in botjh files routes are defined as "router" we can import them with different names to avoid conflict



app = FastAPI()
app.include_router(doctor_router)
app.include_router(welcome_router)












