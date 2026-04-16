from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from app.schemas.models import EmployeeModel, Store


def create_store(
    db: Session,
    name: str,
    cnpj: str,
    phone: str | None = None,
    email: str | None = None,
    zip_code: str | None = None,
    cep: str | None = None,
    city: str | None = None,
    state: str | None = None,
    street: str | None = None,
    address: str | None = None,
    neighborhood: str | None = None,
    number: str | None = None,
    active: bool = True,
):
    effective_zip_code = zip_code if zip_code is not None else cep
    effective_street = street if street is not None else address

    required_fields = {
        "name": name,
        "cnpj": cnpj,
        "phone": phone,
        "email": email,
        "zip_code": effective_zip_code,
        "city": city,
        "state": state,
        "street": effective_street,
        "neighborhood": neighborhood,
        "number": number,
    }
    missing = [field for field, value in required_fields.items() if value in (None, "")]
    if missing:
        raise HTTPException(status_code=400, detail=f"Campos obrigatórios ausentes: {', '.join(missing)}")

    exists_name = db.query(Store).filter(Store.name == name).first()
    exists_cnpj = db.query(Store).filter(Store.cnpj == cnpj).first()

    if exists_name:
        raise HTTPException(status_code=400, detail="Loja já existe com esse nome")
    if exists_cnpj:
        raise HTTPException(status_code=400, detail="Loja já existe com esse CNPJ")
    
    db_store = Store(
        name=name,
        cnpj=cnpj,
        phone=phone,
        email=email,
        zip_code=effective_zip_code,
        city=city,
        state=state,
        street=effective_street,
        neighborhood=neighborhood,
        number=number,
        active=active,
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_store(db: Session, store_id: int):
    store = (
        db.query(Store)
        .options(joinedload(Store.employees).joinedload(EmployeeModel.user))
        .filter(Store.id == store_id)
        .first()
    )
    if not store:
        raise HTTPException(status_code=404, detail="Loja não encontrada")
    return store

def update_store(
    db: Session,
    store_id: int,
    name: str | None = None,
    cnpj: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    zip_code: str | None = None,
    cep: str | None = None,
    city: str | None = None,
    state: str | None = None,
    street: str | None = None,
    address: str | None = None,
    neighborhood: str | None = None,
    number: str | None = None,
    active: bool | None = None,
):
    effective_zip_code = zip_code if zip_code is not None else cep
    effective_street = street if street is not None else address

    store = get_store(db, store_id)
    for field, value in {
        "name": name,
        "cnpj": cnpj,
        "phone": phone,
        "email": email,
        "zip_code": effective_zip_code,
        "city": city,
        "state": state,
        "street": effective_street,
        "neighborhood": neighborhood,
        "number": number,
        "active": active,
    }.items():
        if value is not None:
            setattr(store, field, value)

    db.commit()
    db.refresh(store)
    return store


def delete_store(db: Session, store_id: int):
    store = get_store(db, store_id)
    db.delete(store)
    db.commit()
   


def list_stores(db: Session):
    return db.query(Store).options(joinedload(Store.employees).joinedload(EmployeeModel.user)).all()