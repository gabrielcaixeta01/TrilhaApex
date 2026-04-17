from datetime import datetime
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.models import Appointment, AppointmentService, EmployeeModel, Pet, Service



def _normalize_service_ids(service_ids: list[int | str] | None) -> list[int] | None:
	if service_ids is None:
		return None

	normalized_ids: list[int] = []
	for service_id in service_ids:
		if isinstance(service_id, int):
			normalized_ids.append(service_id)
			continue

		for chunk in service_id.split(","):
			value = chunk.strip()
			if not value:
				continue
			if not value.isdigit():
				raise HTTPException(status_code=422, detail=f"service_ids inválido: {value}")
			normalized_ids.append(int(value))

	return list(dict.fromkeys(normalized_ids))


def _load_services(db: Session, service_ids: list[int | str] | None) -> list[Service] | None:
	normalized_service_ids = _normalize_service_ids(service_ids)
	if normalized_service_ids is None:
		return None
	if not normalized_service_ids:
		return []

	services = db.query(Service).filter(Service.id.in_(normalized_service_ids)).all()
	services_by_id = {service.id: service for service in services}
	missing_service_ids = [service_id for service_id in normalized_service_ids if service_id not in services_by_id]
	if missing_service_ids:
		raise HTTPException(
			status_code=404,
			detail=f"Serviço(s) não encontrado(s): {', '.join(str(service_id) for service_id in missing_service_ids)}",
		)

	return [services_by_id[service_id] for service_id in normalized_service_ids]



def _require_employee_belongs_to_store(db: Session, employee_id: int, store_id: int) -> None:
	employee = (
		db.query(EmployeeModel)
		.filter(EmployeeModel.user_id == employee_id, EmployeeModel.store_id == store_id)
		.first()
	)
	if employee is None:
		raise HTTPException(status_code=400, detail="O funcionário selecionado não pertence à loja informada")


def _calculate_appointment_total(db: Session, appointment_id: int) -> Decimal:
	total = (
		db.query(func.coalesce(func.sum(AppointmentService.charged_value), 0))
		.filter(AppointmentService.appointment_id == appointment_id)
		.scalar()
	)
	return Decimal(total)


def _sync_appointment_total(db: Session, appointment: Appointment) -> Appointment:
	appointment.final_value = _calculate_appointment_total(db, appointment.id)
	return appointment


def create_appointment(
	db: Session,
	service_at: datetime | None = None,
	status: str = "agendado",
	store_id: int | None = None,
	client_id: int | None = None,
	employee_id: int | None = None,
	pet_id: int | None = None,
	payment_method: str | None = None,
	notes: str | None = None,
	online: bool = False,
	service_ids: list[int | str] | None = None,
):
	

	if store_id is None:
		raise HTTPException(status_code=400, detail="Loja é obrigatória")
	if client_id is None:
		raise HTTPException(status_code=400, detail="Cliente é obrigatório")
	if employee_id is None:
		raise HTTPException(status_code=400, detail="Funcionário é obrigatório")
	if pet_id is None:
		raise HTTPException(status_code=400, detail="Pet é obrigatório")
	if not payment_method:
		raise HTTPException(status_code=400, detail="Forma de pagamento é obrigatória")

	_require_employee_belongs_to_store(db, employee_id, store_id)

	if service_ids is None:
		raise HTTPException(status_code=400, detail="Ao menos um serviço é obrigatório")
	services = _load_services(db, service_ids)

	pet = db.query(Pet).filter(Pet.id == pet_id).first()
	if not pet:
		raise HTTPException(status_code=404, detail="Pet não encontrado")

	if pet.owner_id != client_id:
		raise HTTPException(
			status_code=400,
			detail=f"O pet selecionado não pertence ao cliente informado. Pet pertence ao cliente {pet.owner_id}",
		)

	appointment = Appointment(
		final_value=Decimal("0"),
		service_at=service_at or datetime.utcnow(),
		status= status,
		store_id=store_id,
		client_id=client_id,
		employee_id=employee_id,
		pet_id=pet_id,
		payment_method=payment_method,
		notes=notes,
		online=online,
	)
	db.add(appointment)
	db.flush()

	if services is not None:
		for service in services:
			db.add(
				AppointmentService(
					appointment_id=appointment.id,
					service_id=service.id,
					charged_value=service.price,
				)
			)
		db.flush()

	_sync_appointment_total(db, appointment)
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
	employee_id: int | None = None,
	pet_id: int | None = None,
	payment_method: str | None = None,
	notes: str | None = None,
	online: bool | None = None,
	service_ids: list[int | str] | None = None,
):
	
	appointment = get_appointment(db, appointment_id)
	
	if service_ids is None:
		raise HTTPException(status_code=400, detail="Ao menos um serviço é obrigatório")
	services = _load_services(db, service_ids)

	_require_employee_belongs_to_store(db, employee_id, store_id)

	if pet_id is not None:
		pet = db.query(Pet).filter(Pet.id == pet_id).first()
		if not pet:
			raise HTTPException(status_code=404, detail="Pet não encontrado")
		
		effective_client_id = client_id if client_id is not None else appointment.client_id
		if pet.owner_id != effective_client_id:
			raise HTTPException(
				status_code=400,
				detail=f"O pet selecionado não pertence ao cliente informado. Pet pertence ao cliente {pet.owner_id}",
			)

	updates = {
		"service_at": service_at,
		"status": status,
		"store_id": store_id,
		"client_id": client_id,
		"employee_id": employee_id,
		"pet_id": pet_id,
		"payment_method": payment_method,
		"notes": notes,
		"online": online,
	}
	for key, value in updates.items():
		if value is not None:
			setattr(appointment, key, value)

	if services is not None:
		appointment.services.clear()
		db.flush()
		for service in services:
			db.add(
				AppointmentService(
					appointment_id=appointment.id,
					service_id=service.id,
					charged_value=service.price,
				)
			)
		db.flush()

	_sync_appointment_total(db, appointment)

	db.commit()
	db.refresh(appointment)
	return _sync_appointment_total(db, appointment)


def delete_appointment(db: Session, appointment_id: int):
	appointment = get_appointment(db, appointment_id)
	db.delete(appointment)
	db.commit()


def list_appointments( db: Session) -> list[Appointment]:
	return db.query(Appointment).order_by(Appointment.id).all()
