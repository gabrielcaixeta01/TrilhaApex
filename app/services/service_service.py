from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.models import Service


def create_service(
    db: Session,
    name: str,
    description: str | None = None,
    price: float | None = None,
):
    if not name.strip():
        raise HTTPException(status_code=400, detail="Nome do serviço é obrigatório")
    if price is None:
        raise HTTPException(status_code=400, detail="Preço do serviço é obrigatório")
    if price < 0:
        raise HTTPException(status_code=400, detail="Preço do serviço não pode ser negativo")

    service = Service(name=name.strip(), description=description, price=price)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


def update_service(
    db: Session,
    service_id: int,
    name: str | None = None,
    description: str | None = None,
    price: float | None = None,
):
    service = get_service(db, service_id)

    if name is not None:
        if not name.strip():
            raise HTTPException(status_code=400, detail="Nome do serviço é obrigatório")
        service.name = name.strip()
    if description is not None:
        service.description = description
    if price is not None:
        if price < 0:
            raise HTTPException(status_code=400, detail="Preço do serviço não pode ser negativo")
        service.price = price

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int):
    service = get_service(db, service_id)
    db.delete(service)
    db.commit()


def list_services(db: Session) -> list[Service]:
    return db.query(Service).all()