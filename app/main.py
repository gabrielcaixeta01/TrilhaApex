from fastapi import FastAPI
from app.routers.pet_crud import router as pet_router
from app.routers.order_crud import router as order_router
from app.routers.user_crud import router as user_router

app = FastAPI(title="Petstore da Apex")

app.include_router(pet_router)
app.include_router(order_router)
app.include_router(user_router)