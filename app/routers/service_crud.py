from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.service_service import (
    create_service,
    get_service,
    list_services,
    update_service,
    delete_service,
)
from app.schemas.schemas import ServiceCatalog

router = APIRouter(prefix="/service", tags=["CRUD de Serviços"])


@router.post("", status_code=201, response_model=ServiceCatalog)
def criar_servico(
    name: str = Query(...),
    description: str | None = Query(None),
    price: float | None = Query(None),
    db: Session = Depends(get_db),
):
    created = create_service(
        db=db,
        name=name,
        description=description,
        price=price,
    )
    return created


@router.get("", response_model=list[ServiceCatalog])
def listar_servicos(
    name: str | None = Query(None),
    db: Session = Depends(get_db),
) -> list[ServiceCatalog]:
    return list_services(
        db,
        name=name,
    )


@router.get("/{id}", response_model=ServiceCatalog)
def buscar_servico(id: int, db: Session = Depends(get_db)) -> ServiceCatalog:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


@router.put("/{id}", response_model=ServiceCatalog)
def atualizar_servico(
    id: int,
    name: str | None = Query(None),
    description: str | None = Query(None),
    price: float | None = Query(None),
    db: Session = Depends(get_db),
) -> ServiceCatalog:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    return update_service(
        db=db,
        service_id=id,
        name=name,
        description=description,
        price=price,
    )


@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_servico(id: int, db: Session = Depends(get_db)) -> dict:
    service = get_service(db, id)
    if service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    delete_service(db, id)
    return {"message": "Serviço deletado com sucesso"}