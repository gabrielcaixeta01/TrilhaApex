from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
from app.schemas.models import UserModel
from app.services.order_service import (
    create_order,
    delete_order,
    get_order,
    list_inventory,
    list_orders,
    update_order,
)
from app.schemas.schemas import MessageResponse, OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/order", tags=["CRUD de Pedidos"])


@router.get("", response_model=list[OrderResponse])
def listar_pedidos(db: Session = Depends(get_db)) -> list[OrderResponse]:
    return list_orders(db)


@router.post("", status_code=201, response_model=OrderResponse)
def criar_pedido(
    payload: OrderCreate,
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
    db: Session = Depends(get_db),
):
    owner_id_final = payload.owner_id if current_user.role == "admin" and payload.owner_id is not None else current_user.id
    ship_date_final = payload.shipDate or datetime.now()
    
    created_order = create_order(
        db=db,
        petId=payload.petId,
        quantity=payload.quantity,
        shipDate=ship_date_final,
        status=payload.status,
        complete=payload.complete,
        owner_id=owner_id_final,

    )
    return created_order


@router.get("/inventory", response_model=dict)
def buscar_inventario(db: Session = Depends(get_db)) -> dict:
    return list_inventory(db)


@router.get("/{id}", response_model=OrderResponse)
def buscar_pedido(id: int, db: Session = Depends(get_db)) -> OrderResponse:
    order = get_order(db, id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


@router.put("/{id}", response_model=OrderResponse)
def atualizar_pedido(
    id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
) -> OrderResponse:
    order = get_order(db, id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if current_user.role != "admin" and order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o dono do pedido pode atualizar")

    owner_id_final = payload.owner_id
    if current_user.role != "admin":
        owner_id_final = current_user.id

    updated_order = update_order(
        db=db,
        order_id=id,
        petId=payload.petId,
        quantity=payload.quantity,
        shipDate=payload.shipDate,
        status=payload.status,
        complete=payload.complete,
        owner_id=owner_id_final,
    )
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return updated_order


@router.delete("/{id}", status_code=200, response_model=MessageResponse)
def deletar_pedido(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
) -> MessageResponse:
    order = get_order(db, id)
    if order is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if current_user.role != "admin" and order.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o dono do pedido pode deletar")

    delete_order(db, id)
    return {"message": "Pedido deletado com sucesso"}