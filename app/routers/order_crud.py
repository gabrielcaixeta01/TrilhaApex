from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_service import (
    create_order,
    get_order,
    delete_order,
    list_inventory
)

router = APIRouter(prefix="/store", tags=["Store"])


@router.post("/order", status_code=201, response_model=dict)
def criar_pedido(
    order_id: int,
    petId: int,
    quantity: int | None = None,
    shipDate: datetime | None = None,
    status: str = "placed",
    complete: bool = False,
    db: Session = Depends(get_db),
):
    return create_order(
        db=db,
        order_id=order_id,
        petId=petId,
        quantity=quantity,
        shipDate=shipDate,
        status=status,
        complete=complete
    )


@router.get("/order/{order_id}", response_model=dict)
def buscar_pedido(order_id: int, db: Session = Depends(get_db)) -> dict:
    return get_order(db, order_id)


@router.delete("/order/{order_id}", status_code=204)
def deletar_pedido(order_id: int, db: Session = Depends(get_db)):
    delete_order(db, order_id)


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)