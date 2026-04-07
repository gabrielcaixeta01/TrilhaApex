from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.models import UserModel
from app.security import create_access_token, hash_password, verify_password

ALLOWED_ROLES = {"cliente", "funcionario", "admin_loja", "super_admin"}


def _find_user(db: Session, name: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.name == name).first()


def create_user(
    db: Session,
    name: str,
    password: str,
    email: str,
    role: str = "cliente",
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
):
    if len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")

    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")

    if not name.strip():
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")

    exists = db.query(UserModel).filter(UserModel.name == name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    db_user = UserModel(
        name=name.strip(),
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
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, email: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_user(
    db: Session,
    name: str,
    new_name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    phone: str | None = None,
    role: str | None = None,
    user_active: bool | None = None,
):
    user = _find_user(db, name)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if new_name is not None:
        if not new_name.strip():
            raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")
        user.name = new_name.strip()

    if email is not None:
        user.email = email

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


def delete_user(db: Session, name: str):
    user = _find_user(db, name)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()


def login(db: Session, name_or_email: str, password: str):
    user = _find_user(db, name_or_email) or db.query(UserModel).filter(UserModel.email == name_or_email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    if not user.user_active:
        raise HTTPException(status_code=403, detail="Usuário inativo")

    token = create_access_token(subject=user.name, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
    }


def logout():
    return {"message": "ok"}
