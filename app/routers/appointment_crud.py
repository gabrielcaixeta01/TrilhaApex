from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import Appointment
from app.services import appointment_service

router = APIRouter(prefix="/appointment", tags=["CRUD de Atendimentos"])


@router.post("", status_code=201, response_model=Appointment)
def create_appointment(
	service_at: datetime | None = Query(None),
	status: str = Query("agendado"),
	store_id: int = Query(...),
	client_id: int = Query(...),
	employee_id: int | None = Query(None),
	worker_id: int | None = Query(None),
	pet_id: int = Query(...),
	payment_method: str | None = Query(None),
	payment_type: str | None = Query(None),
	notes: str | None = Query(None),
	observations: str | None = Query(None),
	online: bool = Query(False),
	service_ids: list[int] = Query(...),
	db: Session = Depends(get_db),
):
	effective_employee_id = employee_id if employee_id is not None else worker_id
	effective_payment_method = payment_method if payment_method is not None else payment_type
	effective_notes = notes if notes is not None else observations

	return appointment_service.create_appointment(
		db=db,
		service_at=service_at,
		status=status,
		store_id=store_id,
		client_id=client_id,
		employee_id=effective_employee_id,
		pet_id=pet_id,
		payment_method=effective_payment_method,
		notes=effective_notes,
		online=online,
		service_ids=service_ids,
	)


@router.get("/appointments", response_model=list[Appointment])
def list_appointments(db: Session = Depends(get_db)) -> list[Appointment]:
	return appointment_service.list_appointments(db)


@router.get("/{id}", response_model=Appointment)
def get_appointment(id: int, db: Session = Depends(get_db)) -> Appointment:
	return appointment_service.get_appointment(db, id)


@router.put("/{id}", response_model=Appointment)
def update_appointment(
	id: int,
	service_at: datetime | None = Query(None),
	status: str | None = Query(None),
	store_id: int | None = Query(None),
	client_id: int | None = Query(None),
	employee_id: int | None = Query(None),
	worker_id: int | None = Query(None),
	pet_id: int | None = Query(None),
	payment_method: str | None = Query(None),
	payment_type: str | None = Query(None),
	notes: str | None = Query(None),
	observations: str | None = Query(None),
	online: bool | None = Query(None),
	service_ids: list[str] | None = Query(None),
	service_ids_brackets: list[str] | None = Query(None, alias="service_ids[]"),
	db: Session = Depends(get_db),
) -> Appointment:
	raw_service_ids = (service_ids or []) + (service_ids_brackets or [])
	effective_employee_id = employee_id if employee_id is not None else worker_id
	effective_payment_method = payment_method if payment_method is not None else payment_type
	effective_notes = notes if notes is not None else observations

	updated_appointment = appointment_service.update_appointment(
		db=db,
		appointment_id=id,
		service_at=service_at,
		status=status,
		store_id=store_id,
		client_id=client_id,
		employee_id=effective_employee_id,
		pet_id=pet_id,
		payment_method=effective_payment_method,
		notes=effective_notes,
		online=online,
		service_ids=raw_service_ids or None,
	)
	return updated_appointment


@router.delete("/{id}", status_code=200, response_model=dict)
def delete_appointment(id: int, db: Session = Depends(get_db)) -> dict:
	appointment_service.delete_appointment(db, id)
	return {"message": "Atendimento deletado com sucesso"}