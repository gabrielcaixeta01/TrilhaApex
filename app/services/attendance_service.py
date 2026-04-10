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


def _sync_attendance_total(db: Session, attendance: Service) -> Service:
	attendance.value_final = _calculate_attendance_total(db, attendance.id)
	db.commit()
	db.refresh(attendance)
	return attendance


def create_attendance(
	db: Session,
	service_at: datetime | None = None,
	status: str = "agendado",
	store_id: int | None = None,
	client_id: int | None = None,
	worker_id: int | None = None,
	payment_type: str | None = None,
	observations: str | None = None,
	online: bool = False,
):
	if store_id is None:
		raise HTTPException(status_code=400, detail="Loja é obrigatória")
	if client_id is None:
		raise HTTPException(status_code=400, detail="Cliente é obrigatório")
	if worker_id is None:
		raise HTTPException(status_code=400, detail="Funcionário é obrigatório")
	if not payment_type:
		raise HTTPException(status_code=400, detail="Forma de pagamento é obrigatória")

	attendance = Service(
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
	db.add(attendance)
	db.commit()
	db.refresh(attendance)
	return _sync_attendance_total(db, attendance)


def get_attendance(db: Session, attendance_id: int):
	attendance = db.query(Service).filter(Service.id == attendance_id).first()
	if not attendance:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")
	return _sync_attendance_total(db, attendance)


def list_attendances(
	db: Session,
	client_id: int | None = None,
	store_id: int | None = None,
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

	attendances = query.order_by(Service.service_at.desc()).all()
	for attendance in attendances:
		attendance.value_final = _calculate_attendance_total(db, attendance.id)
	db.commit()
	return attendances


def update_attendance(
	db: Session,
	attendance_id: int,
	service_at: datetime | None = None,
	status: str | None = None,
	store_id: int | None = None,
	client_id: int | None = None,
	worker_id: int | None = None,
	payment_type: str | None = None,
	observations: str | None = None,
	online: bool | None = None,
):
	attendance = get_attendance(db, attendance_id)

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
			setattr(attendance, key, value)

	db.commit()
	db.refresh(attendance)
	return _sync_attendance_total(db, attendance)


def delete_attendance(db: Session, attendance_id: int):
	attendance = get_attendance(db, attendance_id)
	db.delete(attendance)
	db.commit()
