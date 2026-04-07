import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.models import Service, Pet, User
from app.security import hash_password, verify_password, create_access_token

ALLOWED_ROLES = {"cliente", "funcionario", "admin_loja", "super_admin"}

def create_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    role: str,
    phone: str | None = None,
    cpf: str | None = None,
    cnpj: str | None = None,
    client_type: str | None = None,
    birth_date: str | None = None,
    address: str | None = None,
    job_title: str | None = None,
    hired_at: str | None = None,
    store_id: int | None = None,
    user_active: bool = True,
    created_at: str | None = None,
):
    
    if len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")
    exists = db.query(User).filter(User.name == name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    db_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        phone=phone,
        cpf=cpf,
        cnpj=cnpj,
        client_type=client_type,
        birth_date=birth_date,
        address=address,
        job_title=job_title,
        hired_at=hired_at,
        store_id=store_id,
        user_active=user_active,
        created_at=created_at,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_user(
    db: Session,
    email: str,
    name: str | None = None,
    password: str | None = None,
    role: str | None = None,
    phone: str | None = None,
    user_active: bool | None = None,

):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if name is not None:
        user.name = name
    if password is not None:
        if len(password.strip()) < 8:
            raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
        user.password_hash = hash_password(password)
    if role is not None:
        if role not in ALLOWED_ROLES:
            raise HTTPException(status_code=400, detail="Role inválida")
        user.role = role
    if phone is not None:
        user.phone = phone
    if user_active is not None:
        user.user_active = user_active

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usu'ário não encontrado")

    db.query(Pet).filter(Pet.owner_id == user.id).update(
        {Pet.owner_id: None}, synchronize_session=False
    )
    db.query(Service).filter(Service.owner_id == user.id).delete(synchronize_session=False)

    db.delete(user)
    db.commit()