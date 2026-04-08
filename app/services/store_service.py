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
    address: str | None = None,
    city: str | None = None,
    state: str | None = None,
    active: bool = True,
):
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
        address=address,
        city=city,
        state=state,
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
    address: str | None = None,
    city: str | None = None,
    state: str | None = None,
    active: bool | None = None,
):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        return None

    if name is not None:
        store.name = name
    if cnpj is not None:
        store.cnpj = cnpj
    if phone is not None:
        store.phone = phone
    if email is not None:
        store.email = email
    if cep is not None:
        store.cep = cep
    if address is not None:
        store.address = address
    if city is not None:
        store.city = city
    if state is not None:
        store.state = state
    if active is not None:
        store.active = active

    db.commit()
    db.refresh(store)
    return store


def delete_store(db: Session, store_id: int):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store:
        db.delete(store)
        db.commit()
    return store