from fastapi import APIRouter
from app.services.user_service import (
    create_user,
    get_user,
    update_user,
    delete_user,
    login,
    logout,
    create_with_list
)

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", status_code=201, response_model=dict)
def criar_user(
    id: int,
    username: str,
    password: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    userStatus: int = 0
) -> dict:
   
    return create_user(
        id=id,
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        email=email,
        phone=phone,
        userStatus=userStatus
    )


@router.get("/{username}", response_model=dict)
def buscar_user(username: str) -> dict:
    return get_user(username)


@router.put("/{username}", response_model=dict)
def atualizar_user(
    username: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    userStatus: int | None = None
) -> dict:
  
    return update_user(
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=password,
        phone=phone,
        userStatus=userStatus
    )


@router.delete("/{username}", status_code=204)
def deletar_user(username: str) -> None:
    delete_user(username)


@router.get("/login", response_model=dict)
def login_user(username: str, password: str) -> dict:
    return login(username, password)


@router.get("/logout", response_model=dict)
def logout_user() -> dict:
    return logout()


@router.post("/createWithList", response_model=list[dict])
def criar_lista_usuarios(users: list[dict]) -> list[dict]:
    return create_with_list(users)
