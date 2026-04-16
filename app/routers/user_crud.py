from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import user_service
from app.schemas.schemas import User
from datetime import date
from decimal import Decimal

router = APIRouter(prefix="/user", tags=["CRUD de Usuários"])


@router.post("", status_code=201, response_model=User)
def create_user(
    name: str = Query(...),
    password: str = Query(...),
    email: str = Query(...),
    phone: str | None = Query(None),
    user_active: bool = Query(True),
    profile_type: str | None = Query(None),
    role: str | None = Query(None),
    cpf: str | None = Query(None),
    cnpj: str | None = Query(None),
    client_type: str | None = Query(None),
    client_zip_code: str | None = Query(None),
    client_cep: str | None = Query(None),
    client_state: str | None = Query(None),
    client_city: str | None = Query(None),
    employee_code: str | None = Query(None),
    matricula: str | None = Query(None),
    job_title: str | None = Query(None),
    salary: Decimal | None = Query(None),
    hired_at: date | None = Query(None),
    store_id: int | None = Query(None),
    db: Session = Depends(get_db),
) -> User:
    effective_profile_type = profile_type if profile_type is not None else role
    effective_client_zip_code = client_zip_code if client_zip_code is not None else client_cep
    effective_employee_code = employee_code if employee_code is not None else matricula

    
    created_user = user_service.create_user(
        db=db,
        name=name,
        password=password,
        email=email,
        phone=phone,
        user_active=user_active,
        profile_type=effective_profile_type,
        role=role,
        cpf=cpf,
        cnpj=cnpj,
        client_type=client_type,
        client_zip_code=effective_client_zip_code,
        client_cep=client_cep,
        client_state=client_state,
        client_city=client_city,
        employee_code=effective_employee_code,
        matricula=matricula,
        job_title=job_title,
        salary=salary,
        hired_at=hired_at,
        store_id=store_id,
    )
    return created_user


@router.get("/users", response_model=list[User])
def list_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    return user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    name: str | None = Query(None),
    email: str | None = Query(None),
    password: str | None = Query(None),
    phone: str | None = Query(None),
    profile_type: str | None = Query(None),
    role: str | None = Query(None),
    cpf: str | None = Query(None),
    cnpj: str | None = Query(None),
    client_type: str | None = Query(None),
    client_zip_code: str | None = Query(None),
    client_cep: str | None = Query(None),
    client_state: str | None = Query(None),
    client_city: str | None = Query(None),
    employee_code: str | None = Query(None),
    matricula: str | None = Query(None),
    job_title: str | None = Query(None),
    salary: Decimal | None = Query(None),
    hired_at: date | None = Query(None),
    store_id: int | None = Query(None),
    user_active: bool | None = Query(None),
    db: Session = Depends(get_db),
) -> User:
    effective_profile_type = profile_type if profile_type is not None else role
    effective_client_zip_code = client_zip_code if client_zip_code is not None else client_cep
    effective_employee_code = employee_code if employee_code is not None else matricula

    
    updated_user = user_service.update_user(
        db=db,
        user_id=user_id,
        name=name,
        email=email,
        password=password,
        phone=phone,
        profile_type=effective_profile_type,
        role=role,
        cpf=cpf,
        cnpj=cnpj,
        client_type=client_type,
        client_zip_code=effective_client_zip_code,
        client_cep=client_cep,
        client_state=client_state,
        client_city=client_city,
        employee_code=effective_employee_code,
        matricula=matricula,
        job_title=job_title,
        salary=salary,
        hired_at=hired_at,
        store_id=store_id,
        user_active=user_active,
    )
    return updated_user


@router.delete("/{user_id}", status_code=200, response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    user_service.delete_user(db, user_id)
    return {"message": "Usuário deletado com sucesso"}
