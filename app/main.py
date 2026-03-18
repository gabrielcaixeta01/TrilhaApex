from fastapi import FastAPI
from app.routers.pet_crud import router as pet_router
from app.routers.order_crud import router as order_router

app = FastAPI(title="Petstore da Apex")

app.include_router(pet_router)
app.include_router(order_router)