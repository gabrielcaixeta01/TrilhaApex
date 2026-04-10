from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import Service
from app.services.attendance_service import (
	create_attendance,
	delete_attendance,
	get_attendance,
	list_attendances,
	update_attendance,
)

router = APIRouter(prefix="/attendance", tags=["CRUD de Atendimentos"])


@router.post("", status_code=201, response_model=Service)
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
	return create_attendance(
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


@router.get("", response_model=list[Service])
def listar_atendimentos(
	client_id: int | None = Query(None),
	store_id: int | None = Query(None),
	worker_id: int | None = Query(None),
	status: str | None = Query(None),
	db: Session = Depends(get_db),
) -> list[Service]:
	return list_attendances(
		db,
		client_id=client_id,
		store_id=store_id,
		worker_id=worker_id,
		status=status,
	)


@router.get("/{id}", response_model=Service)
def buscar_atendimento(id: int, db: Session = Depends(get_db)) -> Service:
	attendance = get_attendance(db, id)
	if attendance is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")
	return attendance


@router.put("/{id}", response_model=Service)
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
) -> Service:
	attendance = get_attendance(db, id)
	if attendance is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")

	return update_attendance(
		db=db,
		attendance_id=id,
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
	attendance = get_attendance(db, id)
	if attendance is None:
		raise HTTPException(status_code=404, detail="Atendimento não encontrado")

	delete_attendance(db, id)
	return {"message": "Atendimento deletado com sucesso"}
