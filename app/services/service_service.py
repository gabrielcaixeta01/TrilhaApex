from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.models import ServiceCatalog


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

    service = ServiceCatalog(name=name.strip(), description=description, price=price)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_service(db: Session, service_id: int):
    service = db.query(ServiceCatalog).filter(ServiceCatalog.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


def list_services(
    db: Session,
    name: str | None = None,
):
    query = db.query(ServiceCatalog)
    if name:
        query = query.filter(ServiceCatalog.name.ilike(f"%{name}%"))
    return query.order_by(ServiceCatalog.name.asc()).all()


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


