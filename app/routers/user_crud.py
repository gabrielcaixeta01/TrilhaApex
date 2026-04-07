from fastapi import APIRouter, Depends, HTTPException, Query
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
from app.schemas.schemas import User, UserCreate, TokenResponse
from app.schemas.models import UserModel
from app.security import get_current_user, require_roles

router = APIRouter(prefix="/user", tags=["CRUD de Usuários"])


@router.post("", status_code=201, response_model=User)
def criar_user(
    name: str = Query(...),
    password: str = Query(...),
    email: str = Query(...),
    phone: str | None = Query(None),
    user_active: bool = Query(True),
    role: str = Query("cliente"),
    db: Session = Depends(get_db),
) -> User:
    
    created_user = create_user(
        db=db,
        name=name,
        password=password,
        email=email,
        phone=phone,
        user_active=user_active,
        role=role,
    )
    return created_user


@router.post("/login", response_model=TokenResponse)
def login_user(
    name: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db),
) -> TokenResponse:
    return login(db, name, password)


@router.post("/logout", response_model=dict)
def logout_user(current_user: UserModel = Depends(get_current_user)) -> dict:
    return logout()


@router.post("/createWithList", response_model=list[User])
def criar_lista_usuarios(users: list[UserCreate], db: Session = Depends(get_db)) -> list[User]:
    payload = [user.model_dump() for user in users]
    return create_with_list(db, payload)


@router.get("/{name}", response_model=User)
def buscar_user(name: str, db: Session = Depends(get_db)) -> User:
    return get_user(db, name)


@router.put("/{name}", response_model=User)
def atualizar_user(
    name: str,
    new_name: str | None = Query(None),
    email: str | None = Query(None),
    password: str | None = Query(None),
    phone: str | None = Query(None),
    role: str | None = Query(None),
    user_active: bool | None = Query(None),
    db: Session = Depends(get_db),
) -> User:
    
    if password is not None and len(password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")
        
    return update_user(
        db=db,
        name=name,
        new_name=new_name,
        email=email,
        password=password,
        phone=phone,
        role=role,
        user_active=user_active,
    )


@router.delete("/{name}", status_code=200, response_model=dict)
def deletar_user(
    name: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["cliente", "funcionario", "admin_loja", "super_admin"]))
) -> dict:
    if current_user.role != "super_admin" and current_user.name != name:
        raise HTTPException(status_code=403, detail="Apenas admin ou o próprio usuário podem deletar")

    delete_user(db, name)
    return {"message": "Usuário deletado com sucesso"}
