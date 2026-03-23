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
    petId: int,
    quantity: int | None = None,
    shipDate: datetime | None = None,
    status: str = "placed",
    complete: bool = False,
    db: Session = Depends(get_db),
):
    order = create_order(
        db=db,
        petId=petId,
        quantity=quantity,
        shipDate=shipDate,
        status=status,
        complete=complete
    )
    return {
        "message": f"Pedido criado com sucesso, Id: {order['id']}",
        "id": order["id"],
    }


@router.get("/order/{id}", response_model=dict)
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> dict:
    return get_order(db, id)


@router.delete("/order/{id}", status_code=204)
def deletar_pedido(id: int, db: Session = Depends(get_db)):
    delete_order(db, id)


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)