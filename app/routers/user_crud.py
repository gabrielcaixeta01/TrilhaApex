from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.models import UserModel
from app.schemas.schemas import (
    LoginRequest,
    MessageResponse,
    TokenResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.security import get_current_user
from app.services.user_service import (
    create_user,
    delete_user_by_id,
    get_user_by_id,
    list_users,
    login,
    logout,
    update_user_by_id,
)

router = APIRouter(prefix="/user", tags=["CRUD de Usuários"])


@router.get("", response_model=list[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)) -> list[UserResponse]:
    return list_users(db)


@router.get("/{id}", response_model=UserResponse)
def buscar_user(id: int, db: Session = Depends(get_db)) -> UserResponse:
    user = get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.post("", status_code=201, response_model=UserResponse)
def criar_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    created_user = create_user(
        db=db,
        username=payload.username,
        password=payload.password,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        phone=payload.phone,
        user_active=payload.user_active,
        role=payload.role,
    )
    return created_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return login(db, payload.username, payload.password)


@router.post("/logout", response_model=MessageResponse)
def logout_user(current_user: UserModel = Depends(get_current_user)) -> MessageResponse:
    return logout()


@router.put("/{id}", response_model=UserResponse)
def atualizar_user(
    id: int,
    payload: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    target_user = get_user_by_id(db, id)
    if target_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if current_user.role != "admin" and current_user.id != id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o próprio usuário podem atualizar")

    updated = update_user_by_id(
        db=db,
        user_id=id,
        username=payload.username,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        role=payload.role,
        user_active=payload.user_active,
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated


@router.delete("/{id}", status_code=200, response_model=MessageResponse)
def deletar_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> MessageResponse:
    if current_user.role != "admin" and current_user.id != id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o próprio usuário podem deletar")

    deleted = delete_user_by_id(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}
