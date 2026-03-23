from fastapi import APIRouter, Depends
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

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", status_code=201, response_model=dict)
def criar_user(
    username: str,
    password: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    userStatus: int = 0,
    db: Session = Depends(get_db),
) -> dict:
    user = create_user(
        db=db,
        username=username,
        password=password,
        firstName=firstName,
        lastName=lastName,
        email=email,
        phone=phone,
        userStatus=userStatus
    )
    return {
        "message": f"User criado com sucesso, Id: {user['id']}",
        "id": user["id"],
    }


@router.get("/{username}", response_model=dict)
def buscar_user(username: str, db: Session = Depends(get_db)) -> dict:
    return get_user(db, username)


@router.put("/{username}", response_model=dict)
def atualizar_user(
    username: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    userStatus: int | None = None,
    db: Session = Depends(get_db),
) -> dict:
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


@router.delete("/{username}", status_code=204)
def deletar_user(username: str, db: Session = Depends(get_db)) -> None:
    delete_user(db, username)


@router.get("/login", response_model=dict)
def login_user(username: str, password: str, db: Session = Depends(get_db)) -> dict:
    return login(db, username, password)


@router.get("/logout", response_model=dict)
def logout_user() -> dict:
    return logout()


@router.post("/createWithList", response_model=list[dict])
def criar_lista_usuarios(users: list[dict], db: Session = Depends(get_db)) -> list[dict]:
    return create_with_list(db, users)
