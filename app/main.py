from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import pet_crud, order_crud, user_crud

app = FastAPI(title="Petstore da Apex")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(pet_crud.router)
app.include_router(order_crud.router)
app.include_router(user_crud.router)

