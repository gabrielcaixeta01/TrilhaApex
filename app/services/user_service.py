import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.models import User
from app.security import hash_password, verify_password, create_access_token


ALLOWED_ROLES = {"admin", "user", "viewer"}


def create_user(
    db: Session,
    username: str,
    password: str,
    role: str,
    firstName: str | None = None,
    lastName: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    userStatus: int = 1,
):
    if not password or not password.strip():
        raise HTTPException(status_code=400, detail="Senha é obrigatória")
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")
    if userStatus not in (0, 1):
        raise HTTPException(status_code=400, detail="userStatus deve ser 0 ou 1")

    exists = db.query(User).filter(User.username == username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    db_user = User(
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password_hash=hash_password(password),
        phone=phone,
        userStatus=userStatus,
        role = role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_with_list(db: Session, users: list[dict]) -> list[User]:
    created: list[User] = []
    for data in users:
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            continue

        role = data.get("role", "user")
        if role not in ALLOWED_ROLES:
            role = "user"

        user_status = data.get("userStatus", 1)
        if user_status not in (0, 1):
            user_status = 1

        exists = db.query(User).filter(User.username == username).first()
        if exists:
            continue

        db_user = User(
            username=username,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            email=data.get("email"),
            password_hash=hash_password(password),
            phone=data.get("phone"),
            userStatus=user_status,
            role=role,
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
        "password_hash": hash_password(password) if password is not None else None,
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
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if user.userStatus != 1:
        raise HTTPException(status_code=403, detail="Usuário inativo")
    token = create_access_token(subject=user.username, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800,
        "session": int(time.time()),
    }


def logout():
    return {"code": 200, "type": "success", "message": "ok"}

