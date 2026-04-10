from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.models import AttendanceService, Service


def _calculate_attendance_total(db: Session, attendance_id: int) -> Decimal:
    total = (
        db.query(func.coalesce(func.sum(AttendanceService.charged_value), 0))
        .filter(AttendanceService.attendance_id == attendance_id)
        .scalar()
    )
    return Decimal(total)


def _sync_attendance_total(db: Session, service: Service) -> Service:
    service.value_final = _calculate_attendance_total(db, service.id)
    db.commit()
    db.refresh(service)
    return service


def create_service(
    db: Session,
    value_final: Decimal | None = None,
    service_at: datetime | None = None,
    status: str = "agendado",
    store_id: int | None = None,
    client_id: int | None = None,
    worker_id: int | None = None,
    payment_type: str | None = None,
    observations: str | None = None,
    online: bool = False,
    service_type: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    discount: Decimal | None = Decimal("0"),
    pet_id: int | None = None,
):
    db_service = Service(
        value_final=Decimal("0"),
        service_at=service_at or datetime.utcnow(),
        payment_type=payment_type or "",
        status=status,
        online=online,
        observations=observations,
        store_id=store_id or 1,
        client_id=client_id or 1,
        worker_id=worker_id or 1,
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return _sync_attendance_total(db, db_service)


def get_service(db: Session, service_id: int):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return _sync_attendance_total(db, service)


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
    if worker_id is not None:
        query = query.filter(Service.worker_id == worker_id)
    if status is not None:
        query = query.filter(Service.status == status)

    services = query.order_by(Service.service_at.desc()).all()
    for service in services:
        service.value_final = _calculate_attendance_total(db, service.id)
    db.commit()
    return services


def update_service(
    db: Session,
    service_id: int,
    value_final: Decimal | None = None,
    service_at: datetime | None = None,
    status: str | None = None,
    store_id: int | None = None,
    client_id: int | None = None,
    worker_id: int | None = None,
    payment_type: str | None = None,
    observations: str | None = None,
    online: bool | None = None,
    service_type: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    discount: Decimal | None = None,
    pet_id: int | None = None,
):
    service = get_service(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    updates = {
        "service_at": service_at,
        "status": status,
        "store_id": store_id,
        "client_id": client_id,
        "worker_id": worker_id,
        "payment_type": payment_type,
        "observations": observations,
        "online": online,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(service, key, value)

    db.commit()
    db.refresh(service)
    return _sync_attendance_total(db, service)


def delete_service(db: Session, service_id: int):
    service = get_service(db, service_id)
    if service:
        db.delete(service)
        db.commit()


