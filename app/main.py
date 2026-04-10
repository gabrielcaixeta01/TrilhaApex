from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import attendance_crud, category_crud, pet_crud, service_crud, tag_crud, user_crud

app = FastAPI(title="Petstore da Apex")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(user_crud.router)
app.include_router(pet_crud.router)
app.include_router(attendance_crud.router)
app.include_router(service_crud.router)
app.include_router(category_crud.router)
app.include_router(tag_crud.router)