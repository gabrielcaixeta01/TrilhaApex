from fastapi import APIRouter
from app.schemas.models import UserSchema, UserCreateSchema
from app.services.user_service import (create_user, get_user, update_user, delete_user, login, logout, createWithList)

router = APIRouter(prefix="/user", tags=["User"])

@router.post("")
def criar_user(username, password, payload: UserCreateSchema):
    return create_user(username, password, payload)

@router.get("/{username}")
def buscar_user(username):
    return get_user(username)

@router.put("/{username}")
def atualizar_user(
    username,
    id: int | None = None,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    userStatus: int | None = None,
):
    updates = {
        "id": id,
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "phone": phone,
        "userStatus": userStatus,
    }
    return update_user(username, updates)

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
