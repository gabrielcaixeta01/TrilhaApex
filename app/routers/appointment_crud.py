from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import Appointment
from app.services import appointment_service

router = APIRouter(prefix="/appointment", tags=["CRUD de Atendimentos"])


@router.post("", status_code=201, response_model=Appointment)
def criar_atendimento(
	service_at: datetime | None = Query(None),
	status: str = Query("agendado"),
	store_id: int = Query(...),
	client_id: int = Query(...),
	worker_id: int = Query(...),
	payment_type: str | None = Query(None),
	observations: str | None = Query(None),
	online: bool = Query(False),
	db: Session = Depends(get_db),
):
	return appointment_service.create_appointment(
		db=db,
		service_at=service_at,
		status=status,
		store_id=store_id,
		client_id=client_id,
		worker_id=worker_id,
		payment_type=payment_type,
		observations=observations,
		online=online,
	)


@router.get("/{id}", response_model=Appointment)
def buscar_atendimento(id: int, db: Session = Depends(get_db)) -> Appointment:
	appointment = appointment_service.get_appointment(db, id)
	if appointment is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")
	return appointment


@router.put("/{id}", response_model=Appointment)
def atualizar_atendimento(
	id: int,
	service_at: datetime | None = Query(None),
	status: str | None = Query(None),
	store_id: int | None = Query(None),
	client_id: int | None = Query(None),
	worker_id: int | None = Query(None),
	payment_type: str | None = Query(None),
	observations: str | None = Query(None),
	online: bool | None = Query(None),
	db: Session = Depends(get_db),
) -> Appointment:
	appointment = appointment_service.get_appointment(db, id)
	if appointment is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")

	return appointment_service.update_appointment(
		db=db,
		appointment_id=id,
		service_at=service_at,
		status=status,
		store_id=store_id,
		client_id=client_id,
		worker_id=worker_id,
		payment_type=payment_type,
		observations=observations,
		online=online,
	)


@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_atendimento(id: int, db: Session = Depends(get_db)) -> dict:
	appointment = appointment_service.get_appointment(db, id)
	if appointment is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")

	appointment_service.delete_appointment(db, id)
	return {"message": "Atendimento deletado com sucesso"}


@router.get("", response_model=list[Appointment])
def listar_atendimentos(db: Session = Depends(get_db)) -> list[Appointment]:
	return appointment_service.list_appointments(db)