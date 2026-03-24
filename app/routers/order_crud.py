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


@router.post("/order", status_code=201, response_model=Order)
def criar_pedido(
    petId: int = Query(...),
    quantity: int = Query(1),
    shipDate: datetime = Query(datetime.now()),
    status: str = Query("placed"),
    complete: bool = Query(False),
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


@router.get("/order/{id}", response_model=Order)
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> Order:
    return get_order(db, id)


@router.delete("/order/{id}", status_code=204)
def deletar_pedido(id: int, db: Session = Depends(get_db)):
    delete_order(db, id)


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)