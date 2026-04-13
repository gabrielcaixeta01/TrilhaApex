from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.models import Appointment, AppointmentService


def _calculate_appointment_total(db: Session, appointment_id: int) -> Decimal:
	total = (
		db.query(func.coalesce(func.sum(AppointmentService.charged_value), 0))
		.filter(AppointmentService.appointment_id == appointment_id)
		.scalar()
	)
	return Decimal(total)


def _sync_appointment_total(db: Session, appointment: Appointment) -> Appointment:
	appointment.value_final = _calculate_appointment_total(db, appointment.id)
	return appointment


def create_appointment(
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

	appointment = Appointment(
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
	db.add(appointment)
	db.commit()
	db.refresh(appointment)
	return _sync_appointment_total(db, appointment)


def get_appointment(db: Session, appointment_id: int):
	appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
	if not appointment:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")
	return _sync_appointment_total(db, appointment)


def update_appointment(
	db: Session,
	appointment_id: int,
	service_at: datetime | None = None,
	status: str | None = None,
	store_id: int | None = None,
	client_id: int | None = None,
	worker_id: int | None = None,
	payment_type: str | None = None,
	observations: str | None = None,
	online: bool | None = None,
):
	appointment = get_appointment(db, appointment_id)

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
			setattr(appointment, key, value)

	db.commit()
	db.refresh(appointment)
	return _sync_appointment_total(db, appointment)


def delete_appointment(db: Session, appointment_id: int):
	appointment = get_appointment(db, appointment_id)
	db.delete(appointment)
	db.commit()


def list_appointments( db: Session) -> list[Appointment]:
	return db.query(Appointment).order_by(Appointment.id).all()
