from fastapi import FastAPI
from app.database import Base, engine
from app.routers import pet_crud, order_crud, user_crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Petstore da Apex")

app.include_router(pet_crud.router)
app.include_router(order_crud.router)
app.include_router(user_crud.router)