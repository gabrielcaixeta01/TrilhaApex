from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.models import UserModel
from app.services.service_service import (
    create_service,
    get_service,
    list_services,
    update_service,
    delete_service,
)
from app.schemas.schemas import Service

router = APIRouter(prefix="/service", tags=["CRUD de Atendimentos"])


@router.post("", status_code=201, response_model=Service)
def criar_atendimento(
    service_type: str = Query(...),
    service_at: datetime | None = Query(None),
    status: str = Query("agendado"),
    store_id: int = Query(...),
    pet_id: int = Query(...),
    client_id: int = Query(...),
    worker_id: int = Query(...),
    description: str | None = Query(None),
    price: float | None = Query(None),
    discount: float = Query(0),
    payment_type: str | None = Query(None),
    observations: str | None = Query(None),
    db: Session = Depends(get_db),
):
    service_at_final = service_at or datetime.now()
    
    created_service = create_service(
        db=db,
        service_type=service_type,
        service_at=service_at_final,
        status=status,
        store_id=store_id,
        pet_id=pet_id,
        client_id=client_id,
        worker_id=worker_id,
        description=description,
        price=price,
        discount=discount,
        payment_type=payment_type,
        observations=observations,
    )
    return created_service


@router.get("", response_model=list[Service])
def listar_atendimentos(
    client_id: int | None = Query(None),
    store_id: int | None = Query(None),
    pet_id: int | None = Query(None),
    worker_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
) -> list[Service]:
    return list_services(
        db,
        client_id=client_id,
        store_id=store_id,
        pet_id=pet_id,
        worker_id=worker_id,
        status=status,
    )


@router.get("/{id}", response_model=Service)
def buscar_atendimento(id: int, db: Session = Depends(get_db)) -> Service:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    return service


@router.put("/{id}", response_model=Service)
def atualizar_atendimento(
    id: int,
    service_type: str | None = Query(None),
    service_at: datetime | None = Query(None),
    status: str | None = Query(None),
    store_id: int | None = Query(None),
    pet_id: int | None = Query(None),
    client_id: int | None = Query(None),
    worker_id: int | None = Query(None),
    description: str | None = Query(None),
    price: float | None = Query(None),
    discount: float | None = Query(None),
    payment_type: str | None = Query(None),
    observations: str | None = Query(None),
    db: Session = Depends(get_db),
) -> Service:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")

    return update_service(
        db=db,
        service_id=id,
        service_type=service_type,
        service_at=service_at,
        status=status,
        store_id=store_id,
        pet_id=pet_id,
        client_id=client_id,
        worker_id=worker_id,
        description=description,
        price=price,
        discount=discount,
        payment_type=payment_type,
        observations=observations,
    )


@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_atendimento(id: int, db: Session = Depends(get_db)) -> dict:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")

    delete_service(db, id)
    return {"message": "Atendimento deletado com sucesso"}