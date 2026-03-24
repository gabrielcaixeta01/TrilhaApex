from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_service import (
    create_order,
    get_order,
    delete_order,
    list_inventory
)
from app.schemas.schemas import Order

router = APIRouter(prefix="/store", tags=["Store"])


@router.post("/order", status_code=201, response_model=Order, summary="Criar novo pedido",
             description="Cria um novo pedido para um pet")
def criar_pedido(
    petId: int = Query(..., description="ID do pet"),
    quantity: int | None = Query(None, description="Quantidade"),
    shipDate: datetime | None = Query(None, description="Data de envio"),
    status: str = Query("placed", description="Status do pedido (placed, approved, delivered)"),
    complete: bool = Query(False, description="Indica se o pedido está completo"),
    db: Session = Depends(get_db),
):
    created_order = create_order(
        db=db,
        petId=petId,
        quantity=quantity,
        shipDate=shipDate,
        status=status,
        complete=complete
    )
    return created_order


@router.get("/order/{id}", response_model=Order, summary="Buscar pedido por ID",
            description="Retorna os detalhes de um pedido específico")
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> Order:
    return get_order(db, id)


@router.delete("/order/{id}", status_code=204, summary="Deletar pedido",
               description="Remove um pedido do sistema")
def deletar_pedido(id: int, db: Session = Depends(get_db)):
    delete_order(db, id)


@router.get("/inventory", response_model=dict, summary="Listar inventário",
            description="Retorna o inventário de pets disponíveis")
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)