from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
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
    owner_id: int | None = Query(None),
    current_user = Depends(require_roles(["admin", "user"])),
    db: Session = Depends(get_db),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    created_order = create_order(
        db=db,
        petId=petId,
        quantity=quantity,
        shipDate=shipDate,
        status=status,
        complete=complete,
        owner_id=owner_id

    )
    return created_order


@router.get("/order/{id}", response_model=Order)
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> Order:
    return get_order(db, id)


@router.delete("/order/{id}", status_code=204)
def deletar_pedido(id: int, db: Session = Depends(get_db), current_user = Depends(require_roles(["admin", "user"]))):
    if not current_user:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    
    delete_order(db, id)


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)