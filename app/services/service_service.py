from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.schemas.models import Service


def create_service(
    db: Session,
    service_type: str,
    service_at: datetime,
    status: str,
    store_id: int,
    pet_id: int,
    client_id: int,
    worker_id: int,
    description: str | None = None,
    price: Decimal | None = None,
    discount: Decimal | None = Decimal("0"),
    payment_type: str | None = None,
    observations: str | None = None,
):
    db_service = Service(
        service_type=service_type,
        description=description,
        service_at=service_at,
        status=status,
        price=price,
        discount=discount,
        payment_type=payment_type,
        observations=observations,
        store_id=store_id,
        pet_id=pet_id,
        client_id=client_id,
        worker_id=worker_id,
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        return None
    return service


def list_services(
    db: Session,
    client_id: int | None = None,
    store_id: int | None = None,
    pet_id: int | None = None,
    worker_id: int | None = None,
    status: str | None = None,
):
    query = db.query(Service)
    if client_id is not None:
        query = query.filter(Service.client_id == client_id)
    if store_id is not None:
        query = query.filter(Service.store_id == store_id)
    if pet_id is not None:
        query = query.filter(Service.pet_id == pet_id)
    if worker_id is not None:
        query = query.filter(Service.worker_id == worker_id)
    if status is not None:
        query = query.filter(Service.status == status)

    return query.order_by(Service.service_at.desc()).all()


def update_service(
    db: Session,
    service_id: int,
    service_type: str | None = None,
    service_at: datetime | None = None,
    status: str | None = None,
    store_id: int | None = None,
    pet_id: int | None = None,
    client_id: int | None = None,
    worker_id: int | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    discount: Decimal | None = None,
    payment_type: str | None = None,
    observations: str | None = None,
):
    service = get_service(db, service_id)
    if not service:
        return None

    updates = {
        "service_type": service_type,
        "service_at": service_at,
        "status": status,
        "store_id": store_id,
        "pet_id": pet_id,
        "client_id": client_id,
        "worker_id": worker_id,
        "description": description,
        "price": price,
        "discount": discount,
        "payment_type": payment_type,
        "observations": observations,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: int):
    service = get_service(db, service_id)
    if service:
        db.delete(service)
        db.commit()


