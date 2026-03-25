import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.models import UserModel
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
    user_active: bool = True,
    current_user: UserModel | None = None,
):
    if not password or not password.strip():
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
    
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")
    
    exists = db.query(UserModel).filter(UserModel.username == username).first()

    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    if (current_user is None or current_user.role != "admin") and role == "admin":
        raise HTTPException(status_code=403, detail="Apenas admin pode criar usuário com role admin")
       

    db_user = UserModel(
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password_hash=hash_password(password),
        phone=phone,
        user_active=user_active,
        role = role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_with_list(
    db: Session,
    users: list[dict],
    current_user: UserModel | None = None,
) -> list[UserModel]:
    created: list[UserModel] = []
    for data in users:
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            continue

        role = data.get("role", "user")
        if role not in ALLOWED_ROLES:
            raise HTTPException(status_code=400, detail=f"Role inválida para usuário {username}")

        user_active = data.get("user_active")
        if user_active is None:
            user_active = data.get("userStatus", 1) == 1

        exists = db.query(UserModel).filter(UserModel.username == username).first()
        if exists:
            continue

        db_user = UserModel(
            username=username,
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            email=data.get("email"),
            password_hash=hash_password(password),
            phone=data.get("phone"),
            user_active=user_active,
            role=role,
        )
        if (current_user is None or current_user.role != "admin") and role == "admin":
            raise HTTPException(status_code=403, detail=f"Apenas admin pode criar usuário com role admin (usuário {username})")
        
        db.add(db_user)
        db.flush()
        created.append(db_user)

    db.commit()
    return created


def get_user(db: Session, username: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
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
    user_active: bool | None = None,
):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    updates = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password_hash": hash_password(password) if password is not None else None,
        "phone": phone,
        "user_active": user_active,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()


def login(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not user.user_active:
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

