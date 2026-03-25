from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal
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
from app.schemas.schemas import User, UserCreate, TokenResponse
from app.schemas.models import UserModel
from app.security import get_current_user, get_current_user_optional, require_roles

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", status_code=201, response_model=User)
def criar_user(
    username: str = Query(...),
    password: str = Query(...),
    firstName: str | None = Query(None),
    lastName: str | None = Query(None),
    email: str | None = Query(None),
    phone: str | None = Query(None),
    user_active: bool = Query(True),
    role: Literal["admin", "user", "viewer"] = Query("user"),
    db: Session = Depends(get_db),
    current_user: UserModel | None = Depends(get_current_user_optional),
) -> User:
    
    if role == "admin" and (current_user is None or current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Apenas admin pode criar usuário com role admin")

    created_user = create_user(
        db=db,
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        email=email,
        phone=phone,
        user_active=user_active,
        role=role,
        current_user=current_user,
    )
    return created_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    username: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db),
) -> TokenResponse:
    return login(db, username, password)


@router.get("/logout", response_model=dict)
def logout_user(current_user: UserModel = Depends(get_current_user)) -> dict:
    return logout()


@router.post("/createWithList", response_model=list[User])
def criar_lista_usuarios(
    users: list[UserCreate],
    db: Session = Depends(get_db),
    current_user: UserModel | None = Depends(get_current_user_optional),
) -> list[User]:
    if any(user.role == "admin" for user in users):
        if current_user is None or current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Apenas admin pode criar usuário com role admin")

    payload = [user.model_dump() for user in users]
    return create_with_list(db, payload, current_user=current_user)


@router.get("/{username}", response_model=User)
def buscar_user(username: str, db: Session = Depends(get_db)) -> User:
    return get_user(db, username)


@router.put("/{username}", response_model=User)
def atualizar_user(
    username: str,
    firstName: str | None = Query(None),
    lastName: str | None = Query(None),
    email: str | None = Query(None),
    password: str | None = Query(None),
    phone: str | None = Query(None),
    user_active: bool | None = Query(None),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
) -> User:
    
    if password is not None and len(password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")
    
    if not (current_user.role == "admin" or current_user.username == username):
        raise HTTPException(status_code=403, detail="Apenas admin ou o próprio usuário podem atualizar os dados")
    
    return update_user(
        db=db,
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=password,
        phone=phone,
        user_active=user_active,
    )


@router.delete("/{username}", status_code=204)
def deletar_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"]))
) -> None:
    if current_user.role != "admin" and current_user.username != username:
        raise HTTPException(status_code=403, detail="Apenas admin ou o próprio usuário podem deletar")

    delete_user(db, username)
