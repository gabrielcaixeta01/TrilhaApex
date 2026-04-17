from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import service_service
from app.schemas.schemas import Service

router = APIRouter(prefix="/service", tags=["CRUD de Serviços"])


@router.post("", status_code=201, response_model=Service)
def create_service(
    name: str = Query(...),
    description: str | None = Query(None),
    price: float | None = Query(None),
    db: Session = Depends(get_db),
):
    created = service_service.create_service(
        db=db,
        name=name,
        description=description,
        price=price,
    )
    return created


@router.get("/services", response_model=list[Service])
def list_services(db: Session = Depends(get_db)) -> list[Service]:
    return service_service.list_services(db)


@router.get("/{id}", response_model=Service)
def get_service(id: int, db: Session = Depends(get_db)) -> Service:
   return service_service.get_service(db, id)


@router.put("/{id}", response_model=Service)
def update_service(
    id: int,
    name: str | None = Query(None),
    description: str | None = Query(None),
    price: float | None = Query(None),
    db: Session = Depends(get_db),
) -> Service:
    updated_service = service_service.update_service(
        db=db,
        service_id=id,
        name=name,
        description=description,
        price=price,
    )
    return updated_service


@router.delete("/{id}", status_code=200, response_model=dict)
def delete_service(id: int, db: Session = Depends(get_db)) -> dict:
    service_service.delete_service(db, id)
    return {"message": "Serviço deletado com sucesso"}