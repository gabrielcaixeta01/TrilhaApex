from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import user_service
from app.schemas.schemas import User

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
    
    created_user = user_service.create_user(
        db=db,
        name=name,
        password=password,
        email=email,
        phone=phone,
        user_active=user_active,
        role=role,
    )
    return created_user


@router.get("/users", response_model=list[User])
def listar_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=User)
def buscar_user(user_id: int, db: Session = Depends(get_db)) -> User:
    return user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=User)
def atualizar_user(
    user_id: int,
    name: str | None = Query(None),
    email: str | None = Query(None),
    password: str | None = Query(None),
    phone: str | None = Query(None),
    role: str | None = Query(None),
    user_active: bool | None = Query(None),
    db: Session = Depends(get_db),
) -> User:
    
    if password is not None and len(password) < 8:
        raise HTTPException(status_code=400, detail="A senha deve ter pelo menos 8 caracteres")
        
    return user_service.update_user(
        db=db,
        user_id=user_id,
        name=name,
        email=email,
        password=password,
        phone=phone,
        role=role,
        user_active=user_active,
    )


@router.delete("/{user_id}", status_code=200, response_model=dict)
def deletar_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    user_service.delete_user(db, user_id)
    return {"message": "Usuário deletado com sucesso"}
