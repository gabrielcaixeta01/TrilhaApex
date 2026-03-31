from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
from app.schemas.models import UserModel
from app.services.order_service import (
    create_order,
    get_order,
    delete_order,
    list_inventory
)
from app.schemas.schemas import Order

router = APIRouter(prefix="/order", tags=["CRUD de Pedidos"])


@router.post("", status_code=201, response_model=Order)
def criar_pedido(
    petId: int = Query(...),
    quantity: int = Query(1),
    shipDate: datetime | None = Query(None),
    status: str = Query("placed"),
    complete: bool = Query(False),
    owner_id: int | None = Query(None),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
    db: Session = Depends(get_db),
):
    owner_id_final = owner_id if current_user.role == "admin" and owner_id is not None else current_user.id
    ship_date_final = shipDate or datetime.now()
    
    created_order = create_order(
        db=db,
        petId=petId,
        quantity=quantity,
        shipDate=ship_date_final,
        status=status,
        complete=complete,
        owner_id=owner_id_final

    )
    return created_order


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)


@router.get("/{id}", response_model=Order)
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> Order:
    order = get_order(db, id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
) -> dict:
    order = get_order(db, id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if current_user.role != "admin" and order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o dono do pedido pode deletar")

    delete_order(db, id)
    return {"message": "Pedido deletado com sucesso"}