from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.schemas.models import ClientModel, EmployeeModel, UserModel


ALLOWED_PROFILE_TYPES = {"cliente", "funcionario"}



def create_user(
    db: Session,
    name: str,
    email: str,
    password_hash: str,
    phone: str,
    profile_type: str,
    cpf: str | None = None,
    cnpj: str | None = None,
    active: bool = True,
    is_superuser: bool = False,
    created_at: date | None = None,
    client_type: str | None = None,
    cep: str | None = None,
    state: str | None = None,
    city: str | None = None,
    employee_code: str | None = None,
    job_title: str | None = None,
    salary: Decimal | None = None,
    hired_at: date | None = None,
    store_id: int | None = None,
):
   
    name = name.strip() if name else name

    if profile_type is not None and profile_type not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Perfil inválido. Use 'cliente' ou 'funcionario'")

    if not name:
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")
   
    exists_email = db.query(UserModel).filter(UserModel.email == email).first()
    if exists_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")


    db_user = UserModel(
        name=name,
        email=email,
        password_hash=password_hash,
        phone=phone,
        profile_type=profile_type,
        cpf=cpf,
        cnpj=cnpj,
        active=active,
        is_superuser=is_superuser,
        created_at=created_at or date.today(),
    )


    db.add(db_user)
    db.flush()

    if profile_type == "cliente":
        if any(value is not None for value in [employee_code, job_title, salary, hired_at, store_id]):
            raise HTTPException(
                status_code=400,
                detail="Campos de funcionário devem ser nulos quando o perfil for 'cliente'",
            )
        db.add(
            ClientModel(
                user_id=db_user.id,
                client_type=client_type,
                cep=cep,
                state=state,
                city=city,
            )
        )

    if profile_type == "funcionario":
        if any(value is not None for value in [client_type, cep, state, city]):
            raise HTTPException(
                status_code=400,
                detail="Campos de cliente devem ser nulos quando o perfil for 'funcionario'",
            )
        db.add(
            EmployeeModel(
                user_id=db_user.id,
                employee_code=employee_code,
                job_title=job_title,
                salary=salary,
                hired_at=hired_at,
                store_id=store_id,
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
        password_hash: str | None = None,
        phone: str | None = None,
        profile_type: str | None = None,
        cpf: str | None = None,
        cnpj: str | None = None,
        active: bool = True,
        is_superuser: bool = False,
        client_type: str | None = None,
        cep: str | None = None,
        state: str | None = None,
        city: str | None = None,
        employee_code: str | None = None,
        job_title: str | None = None,
        salary: Decimal | None = None,
        hired_at: date | None = None,
        store_id: int | None = None,
    ):

    user = get_user(db, user_id=user_id)

    if profile_type is not None and profile_type not in ALLOWED_PROFILE_TYPES:
        raise HTTPException(status_code=400, detail="Perfil inválido. Use 'cliente' ou 'funcionario'")

    if name is not None and not name.strip():
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")

    if email is not None:
        exists_email = (db.query(UserModel).filter(UserModel.email == email, UserModel.id != user_id).first())
        if exists_email:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")


    if profile_type == "cliente" and any(value is not None for value in [employee_code, job_title, salary, hired_at, store_id]):
        raise HTTPException(
            status_code=400,
            detail="Campos de funcionário devem ser nulos quando o perfil for 'cliente'",
        )

    if profile_type == "funcionario" and any(value is not None for value in [client_type, cep, state, city]):
        raise HTTPException(
            status_code=400,
            detail="Campos de cliente devem ser nulos quando o perfil for 'funcionario'",
        )
    
    for field, value in {
        "name": name,
        "email": email,
        "password_hash": password_hash,
        "phone": phone,
        "profile_type": profile_type,
        "cpf": cpf,
        "cnpj": cnpj,
        "active": active,
        "is_superuser": is_superuser,
    }.items():
        if value is not None:
            setattr(user, field, value)

    if profile_type == "cliente":
        if user.employee_profile is not None:
            db.delete(user.employee_profile)
            user.employee_profile = None

        if user.client_profile is None:
            user.client_profile = ClientModel(
                user_id=user.id,
                client_type=client_type,
                cep=cep,
                state=state,
                city=city,
            )
        else:
            if client_type is not None:
                user.client_profile.client_type = client_type
            if cep is not None:
                user.client_profile.cep = cep
            if state is not None:
                user.client_profile.state = state
            if city is not None:
                user.client_profile.city = city

    if profile_type == "funcionario":
        if user.client_profile is not None:
            db.delete(user.client_profile)
            user.client_profile = None

        if user.employee_profile is None:
            user.employee_profile = EmployeeModel(
                user_id=user.id,
                employee_code=employee_code,
                job_title=job_title,
                salary=salary,
                hired_at=hired_at,
                store_id=store_id,
            )
        else:
            if employee_code is not None:
                user.employee_profile.employee_code = employee_code
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