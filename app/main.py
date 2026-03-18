from fastapi import FastAPI
from app.routers.pet_crud import router as pet_router

app = FastAPI(title="Petstore da Apex")

app.include_router(pet_router)