import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.models import User


def create_user(
    db: Session,
    username: str,
    password: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    userStatus: int = 1,
):
    exists = db.query(User).filter(User.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    db_user = User(
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=password,
        phone=phone,
        userStatus=userStatus,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_with_list(db: Session, users: list[dict]) -> list[User]:
    created: list[User] = []
    for data in users:
        username = data.get("username")
        if not username:
            continue

        exists = db.query(User).filter(User.username == username).first()
        if exists:
            continue

        db_user = User(
            username=username,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            email=data.get("email"),
            password=data.get("password", ""),
            phone=data.get("phone"),
            userStatus=data.get("userStatus", 1),
        )
        db.add(db_user)
        db.flush()
        created.append(db_user)

    db.commit()
    return created


def get_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_user(
    db: Session,
    username: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    userStatus: int | None = None,
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    updates = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "phone": phone,
        "userStatus": userStatus,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()


def login(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {
        "code": 200,
        "type": "success",
        "message": f"logged in user session:{int(time.time())}",
    }


def logout():
    return {"code": 200, "type": "success", "message": "ok"}

