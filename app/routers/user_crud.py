"""
Router para operações de Users (CRUD)
Endpoints documentados automaticamente no Swagger
"""
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
    firstName: str,
    lastName: str,
    email: str,
    phone: str | None = None,
    userStatus: int = 0
) -> dict:
    """
    Criar um novo usuário
    
    - **username**: Nome de usuário único
    - **email**: Email único
    - **password**: Senha (será armazenada de forma segura)
    """
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
    """
    Buscar um usuário específico por username
    
    - **username**: Nome de usuário
    """
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
    """
    Atualizar informações de um usuário
    
    - **username**: Nome de usuário a atualizar
    """
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
    """
    Deletar um usuário
    
    - **username**: Nome de usuário a deletar
    """
    delete_user(username)


@router.post("/login", response_model=dict)
def login_user(username: str, password: str) -> dict:
    """
    Fazer login do usuário
    
    - **username**: Nome de usuário
    - **password**: Senha
    """
    return login(username, password)


@router.post("/logout", response_model=dict)
def logout_user() -> dict:
    """Fazer logout do usuário"""
    return logout()


@router.post("/createWithList", response_model=list[dict])
def criar_lista_usuarios(users: list[dict]) -> list[dict]:
    """
    Criar múltiplos usuários em uma única operação
    """
    return create_with_list(users)
