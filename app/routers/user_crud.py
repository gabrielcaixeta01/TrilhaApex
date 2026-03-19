from fastapi import APIRouter
from app.schemas.user import UserSchema
from app.services.user_service import (create_user, get_user, update_user, delete_user, login, logout, createWithList)

router = APIRouter(prefix="/user", tags=["User"])

@router.post("")
def criar_user(user_id, payload: UserSchema):
    return create_user(user_id, payload)

@router.get("/{username}")
def buscar_user(username):
    return get_user(username)

@router.put("/{username}")
def atualizar_user(username):
    return update_user(username)

@router.delete("/{username}", status_code=204)
def deletar_user(username):
    return delete_user(username)

@router.get("/login")
def login(username, password):
    return login(username, password)

@router.get("/logout")
def logout():
    return logout()

@router.post("/createWithList")
def criar_lista_Usuarios(users: list[UserSchema]):
    return createWithList(users)

@router.post("/createWithArray")
def criar_lista_Usuarios(users: list[UserSchema]):
    return createWithList(users)