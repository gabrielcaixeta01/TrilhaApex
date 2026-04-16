from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.schemas.models import ClientModel, EmployeeModel, UserModel


ALLOWED_PROFILE_TYPES = {"client", "employee"}


def _normalize_profile_type(profile_type: str | None, default: str = "client") -> str:
    if profile_type is None:
        return default
    profile_map = {
        "cliente": "client",
        "funcionario": "employee",
    }
    return profile_map.get(profile_type, profile_type)

def create_user(
    db: Session,
    name: str,
    password: str,
    email: str,
    profile_type: str = "client",
    role: str | None = None,
    phone: str | None = None,
    cpf: str | None = None,
    cnpj: str | None = None,
    client_type: str | None = None,
    client_zip_code: str | None = None,
    client_cep: str | None = None,
    client_state: str | None = None,
    client_city: str | None = None,
    employee_code: str | None = None,
    matricula: str | None = None,
    job_title: str | None = None,
    salary: Decimal | None = None,
    hired_at: date | None = None,
    store_id: int | None = None,
    active: bool = True,
    is_superuser: bool = False,
    user_active: bool | None = None,
):
    effective_profile_type = _normalize_profile_type(role if role is not None else profile_type)
    effective_client_zip_code = client_zip_code if client_zip_code is not None else client_cep
    effective_employee_code = employee_code if employee_code is not None else matricula

    if len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")

    if effective_profile_type not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Perfil inválido. Use 'cliente' ou 'funcionario'")

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
        profile_type=effective_profile_type,
        phone=phone or "",
        cpf=cpf,
        cnpj=cnpj,
        active=active,
        is_superuser=is_superuser,
    )

    db.add(db_user)
    db.flush()

    if effective_profile_type == "client":
        if any(value is not None for value in [effective_employee_code, job_title, salary, hired_at, store_id]):
            raise HTTPException(
                status_code=400,
                detail="Campos de funcionário devem ser nulos quando o perfil for 'cliente'",
            )
        db.add(
            ClientModel(
                user_id=db_user.id,
                client_type=client_type or "cliente",
                zip_code=effective_client_zip_code or "",
                state=client_state or "",
                city=client_city or "",
            )
        )

    if effective_profile_type == "employee":
        if any(value is not None for value in [client_type, effective_client_zip_code, client_state, client_city]):
            raise HTTPException(
                status_code=400,
                detail="Campos de cliente devem ser nulos quando o perfil for 'funcionario'",
            )
        db.add(
            EmployeeModel(
                user_id=db_user.id,
                employee_code=effective_employee_code or f"EMP-{db_user.id}",
                job_title=job_title or effective_profile_type,
                salary=salary or Decimal("0"),
                hired_at=hired_at or date.today(),
                store_id=store_id or 1,
            )
        )

    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    user = (
        db.query(UserModel)
        .options(joinedload(UserModel.client_profile), joinedload(UserModel.employee_profile))
        .filter(UserModel.id == user_id)
        .first()
    )
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
    profile_type: str | None = None,
    role: str | None = None,
    cpf: str | None = None,
    cnpj: str | None = None,
    client_type: str | None = None,
    client_zip_code: str | None = None,
    client_cep: str | None = None,
    client_state: str | None = None,
    client_city: str | None = None,
    employee_code: str | None = None,
    matricula: str | None = None,
    job_title: str | None = None,
    salary: Decimal | None = None,
    hired_at: date | None = None,
    store_id: int | None = None,
    user_active: bool | None = None,
    is_superuser: bool | None = None,
):
    user = get_user(db, user_id)

    effective_profile_type_input = _normalize_profile_type(role if role is not None else profile_type, default=user.profile_type)
    effective_client_zip_code_input = client_zip_code if client_zip_code is not None else client_cep
    effective_employee_code_input = employee_code if employee_code is not None else matricula

    if password is not None and len(password.strip()) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")

    if effective_profile_type_input not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Perfil inválido. Use 'cliente' ou 'funcionario'")

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

    target_profile_type = effective_profile_type_input

    if target_profile_type == "client" and any(value is not None for value in [effective_employee_code_input, job_title, salary, hired_at, store_id]):
        raise HTTPException(
            status_code=400,
            detail="Campos de funcionário devem ser nulos quando o perfil for 'cliente'",
        )

    if target_profile_type == "employee" and any(value is not None for value in [client_type, effective_client_zip_code_input, client_state, client_city]):
        raise HTTPException(
            status_code=400,
            detail="Campos de cliente devem ser nulos quando o perfil for 'funcionario'",
        )
    
    for field, value in {
        "name": name.strip() if name is not None else None,
        "email": email,
        "password_hash": password,
        "phone": new_phone or phone,
        "profile_type": effective_profile_type_input if (profile_type is not None or role is not None) else None,
        "cpf": cpf,
        "cnpj": cnpj,
        "active": user_active,
        "is_superuser": is_superuser,
    }.items():
        if value is not None:
            setattr(user, field, value)

    if target_profile_type == "client":
        if user.employee_profile is not None:
            db.delete(user.employee_profile)
            user.employee_profile = None

        if user.client_profile is None:
            user.client_profile = ClientModel(
                user_id=user.id,
                client_type=client_type or "cliente",
                zip_code=effective_client_zip_code_input or "",
                state=client_state or "",
                city=client_city or "",
            )
        else:
            if client_type is not None:
                user.client_profile.client_type = client_type
            if effective_client_zip_code_input is not None:
                user.client_profile.zip_code = effective_client_zip_code_input
            if client_state is not None:
                user.client_profile.state = client_state
            if client_city is not None:
                user.client_profile.city = client_city

    if target_profile_type == "employee":
        if user.client_profile is not None:
            db.delete(user.client_profile)
            user.client_profile = None

        if user.employee_profile is None:
            user.employee_profile = EmployeeModel(
                user_id=user.id,
                employee_code=effective_employee_code_input or f"EMP-{user.id}",
                job_title=job_title or "employee",
                salary=salary or Decimal("0"),
                hired_at=hired_at or date.today(),
                store_id=store_id or 1,
            )
        else:
            if effective_employee_code_input is not None:
                user.employee_profile.employee_code = effective_employee_code_input
            if job_title is not None:
                user.employee_profile.job_title = job_title
            if salary is not None:
                user.employee_profile.salary = salary
            if hired_at is not None:
                user.employee_profile.hired_at = hired_at
            if store_id is not None:
                user.employee_profile.store_id = store_id

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id=user_id)
    db.delete(user)
    db.commit()

def list_users(db: Session) -> list[UserModel]:
    return (
        db.query(UserModel)
        .options(joinedload(UserModel.client_profile), joinedload(UserModel.employee_profile))
        .order_by(UserModel.name.asc())
        .all()
    )