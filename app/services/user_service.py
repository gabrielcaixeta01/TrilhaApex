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
    new_password: str | None = None,
    new_phone: str | None = None,
    phone: str | None = None,
    role: str | None = None,
    user_active: bool | None = None,
    is_superuser: bool | None = None,
):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

    if role is not None:
        if role not in ALLOWED_ROLES:
            raise HTTPException(status_code=400, detail="Role inválida")
        user.role = role

    password_to_use = new_password or password
    if password_to_use is not None:
        if len(password_to_use.strip()) < 8:
            raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
        user.password_hash = password_to_use

    phone_to_use = new_phone if new_phone is not None else phone
    if phone_to_use is not None:
        user.phone = phone_to_use

    if user_active is not None:
        user.active = user_active

    if is_superuser is not None:
        user.is_superuser = is_superuser

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(user)
    db.commit()


def create_with_list(db: Session, users: list[dict]):
    created_users = []
    for user_data in users:
        created_users.append(
            create_user(
                db=db,
                name=user_data["name"],
                password=user_data["password"],
                email=user_data["email"],
                role=user_data.get("role", "cliente"),
                phone=user_data.get("phone"),
                cpf=user_data.get("cpf"),
                cnpj=user_data.get("cnpj"),
                client_type=user_data.get("client_type"),
                client_cep=user_data.get("client_cep"),
                client_state=user_data.get("client_state"),
                client_city=user_data.get("client_city"),
                matricula=user_data.get("matricula"),
                job_title=user_data.get("job_title"),
                salary=user_data.get("salary"),
                hired_at=user_data.get("hired_at"),
                store_id=user_data.get("store_id"),
                active=user_data.get("active", True),
                is_superuser=user_data.get("is_superuser", False),
            )
        )
    return created_users

