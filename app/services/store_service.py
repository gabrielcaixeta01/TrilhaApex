from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.models import Store


def create_store(
    db: Session,
    name: str,
    cnpj: str,
    phone: str | None = None,
    email: str | None = None,
    cep: str | None = None,
    city: str | None = None,
    state: str | None = None,
    address: str | None = None,
    neighborhood: str | None = None,
    number: str | None = None,
    active: bool = True,
):
    required_fields = {
        "name": name,
        "cnpj": cnpj,
        "phone": phone,
        "email": email,
        "cep": cep,
        "city": city,
        "state": state,
        "address": address,
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
        cep=cep,
        city=city,
        state=state,
        address=address,
        neighborhood=neighborhood,
        number=number,
        active=active,
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_store(db: Session, store_id: int):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return None
    return store

def update_store(
    db: Session,
    store_id: int,
    name: str | None = None,
    cnpj: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    cep: str | None = None,
    city: str | None = None,
    state: str | None = None,
    address: str | None = None,
    neighborhood: str | None = None,
    number: str | None = None,
    active: bool | None = None,
):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return None

    for field, value in {
        "name": name,
        "cnpj": cnpj,
        "phone": phone,
        "email": email,
        "cep": cep,
        "city": city,
        "state": state,
        "address": address,
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
    store = db.query(Store).filter(Store.id == store_id).first()
    if store:
        db.delete(store)
        db.commit()
    return store


def list_stores(db: Session):
    return db.query(Store).all()