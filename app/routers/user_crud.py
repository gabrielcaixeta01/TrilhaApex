from fastapi import APIRouter
from app.schemas.models import UserSchema
from app.services.user_service import (create_user, get_user, update_user, delete_user, login, logout, createWithList)

router = APIRouter(prefix="/user", tags=["User"])

@router.post("")
def criar_user(payload: UserSchema):
    return create_user(payload)

@router.get("/{username}")
def buscar_user(username):
    return get_user(username)

@router.put("/{username}")
def atualizar_user(username, payload: UserSchema):
    return update_user(username, payload)

@router.delete("/{username}", status_code=204)
def deletar_user(username):
    return delete_user(username)

@router.get("/login")
def login_user(username, password):
    return login(username, password)

@router.get("/logout")
def logout_user():
    return logout()

@router.post("/createWithList")
def criar_lista_Usuarios(users: list[UserSchema]):
    return createWithList(users)
