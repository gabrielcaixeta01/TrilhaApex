from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import (
    create_user,
    get_user,
    update_user,
    delete_user,
    login,
    logout,
    create_with_list
)
from app.schemas.schemas import UserResponse, UserCreate

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", status_code=201, response_model=UserResponse, summary="Criar novo usuário", 
             description="Cria um novo usuário no sistema")
def criar_user(
    username: str = Query(..., description="Nome de usuário único"),
    password: str = Query(..., description="Senha do usuário"),
    firstName: str | None = Query(None, description="Primeiro nome"),
    lastName: str | None = Query(None, description="Último nome"),
    email: str | None = Query(None, description="Email do usuário"),
    phone: str | None = Query(None, description="Número de telefone"),
    userStatus: int = Query(1, description="Status do usuário (0=inativo, 1=ativo)"),
    db: Session = Depends(get_db),
) -> UserResponse:
    created_user = create_user(
        db=db,
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        email=email,
        phone=phone,
        userStatus=userStatus
    )
    return created_user


@router.get("/login", response_model=dict, summary="Login de usuário",
            description="Realiza login com username e password")
def login_user(
    username: str = Query(..., description="Nome de usuário"),
    password: str = Query(..., description="Senha do usuário"),
    db: Session = Depends(get_db),
) -> dict:
    return login(db, username, password)


@router.get("/logout", response_model=dict, summary="Logout de usuário",
            description="Realiza logout do usuário")
def logout_user() -> dict:
    return logout()


@router.post("/createWithList", response_model=list[UserResponse], summary="Criar múltiplos usuários",
             description="Cria uma lista de usuários de uma vez")
def criar_lista_usuarios(users: list[UserCreate], db: Session = Depends(get_db)) -> list[UserResponse]:
    payload = [user.model_dump() for user in users]
    return create_with_list(db, payload)


@router.get("/{username}", response_model=UserResponse, summary="Buscar usuário",
            description="Busca um usuário pelo nome de usuário")
def buscar_user(username: str, db: Session = Depends(get_db)) -> UserResponse:
    return get_user(db, username)


@router.put("/{username}", response_model=UserResponse, summary="Atualizar usuário",
            description="Atualiza os dados de um usuário existente")
def atualizar_user(
    username: str,
    firstName: str | None = Query(None, description="Primeiro nome"),
    lastName: str | None = Query(None, description="Último nome"),
    email: str | None = Query(None, description="Email do usuário"),
    password: str | None = Query(None, description="Senha do usuário"),
    phone: str | None = Query(None, description="Número de telefone"),
    userStatus: int | None = Query(None, description="Status do usuário"),
    db: Session = Depends(get_db),
) -> UserResponse:
    return update_user(
        db=db,
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=password,
        phone=phone,
        userStatus=userStatus
    )


@router.delete("/{username}", status_code=204, summary="Deletar usuário",
               description="Remove um usuário do sistema")
def deletar_user(username: str, db: Session = Depends(get_db)) -> None:
    delete_user(db, username)
