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
    if store_id is None:
        raise HTTPException(status_code=400, detail="Loja é obrigatória")
    if client_id is None:
        raise HTTPException(status_code=400, detail="Cliente é obrigatório")
    if worker_id is None:
        raise HTTPException(status_code=400, detail="Funcionário é obrigatório")
    if not payment_type:
        raise HTTPException(status_code=400, detail="Forma de pagamento é obrigatória")

    db_service = Service(
        value_final=Decimal("0"),
        service_at=service_at or datetime.utcnow(),
        payment_type=payment_type,
        status=status,
        online=online,
        observations=observations,
        store_id=store_id,
        client_id=client_id,
        worker_id=worker_id,
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


def update_service(
    db: Session,
    service_id: int,
    service_at: datetime | None = None,
    status: str | None = None,
    store_id: int | None = None,
    client_id: int | None = None,
    worker_id: int | None = None,
    payment_type: str | None = None,
    observations: str | None = None,
    online: bool | None = None,
    
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


