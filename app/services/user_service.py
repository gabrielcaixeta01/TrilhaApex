from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.models import ClientModel, EmployeeModel, UserModel

ALLOWED_ROLES = {"cliente", "funcionario", "admin_loja", "super_admin"}

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
    client_cep: str | None = None,
    client_state: str | None = None,
    client_city: str | None = None,
    matricula: str | None = None,
    job_title: str | None = None,
    salary: Decimal | None = None,
    hired_at: date | None = None,
    store_id: int | None = None,
    active: bool = True,
    is_superuser: bool = False,
    user_active: bool | None = None,
):
    if len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")

    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")

    if not name.strip():
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")

   
    exists_email = db.query(UserModel).filter(UserModel.email == email).first()
    if exists_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    if user_active is not None:
        active = user_active

    db_user = UserModel(
        name=name.strip(),
        email=email,
        password_hash=password,
        role=role,
        phone=phone or "",
        cpf=cpf,
        cnpj=cnpj,
        active=active,
        is_superuser=is_superuser,
    )

    db.add(db_user)
    db.flush()

    if role == "cliente" or client_type is not None:
        db.add(
            ClientModel(
                user_id=db_user.id,
                client_type=client_type or "cliente",
                cep=client_cep or "",
                state=client_state or "",
                city=client_city or "",
            )
        )

    if role in {"funcionario", "admin_loja"} or job_title is not None or store_id is not None:
        db.add(
            EmployeeModel(
                user_id=db_user.id,
                matricula=matricula or f"USR-{db_user.id}",
                job_title=job_title or role,
                salary=salary or Decimal("0"),
                hired_at=hired_at or date.today(),
                store_id=store_id or 1,
            )
        )

    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user




def update_user(
    db: Session,
    user_id: int,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    new_phone: str | None = None,
    phone: str | None = None,
    role: str | None = None,
    user_active: bool | None = None,
    is_superuser: bool | None = None,
):
    user = get_user(db, user_id)

    if password is not None and len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")

    if role is not None and role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Role inválida")

    if name is not None and not name.strip():
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")

    if email is not None:
        exists_email = (
            db.query(UserModel)
            .filter(UserModel.email == email, UserModel.id != user_id)
            .first()
        )
        if exists_email:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    for field, value in {
        "name": name.strip() if name is not None else None,
        "email": email,
        "password_hash": password,
        "phone": new_phone or phone,
        "role": role,
        "active": user_active,
        "is_superuser": is_superuser,
    }.items():
        if value is not None:
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id=user_id)
    db.delete(user)
    db.commit()

def list_users(db: Session) -> list[UserModel]:
    return db.query(UserModel).order_by(UserModel.name.asc()).all()