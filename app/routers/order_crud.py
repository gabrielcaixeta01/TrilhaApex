from fastapi import APIRouter
from app.schemas.models import OrderSchema
from app.services.order_service import (create_order, get_order, delete_order, list_inventory)

router = APIRouter(prefix="/store", tags=["Store"])

@router.post("/order", status_code=201)
def criar_pedido(payload: OrderSchema):
    return create_order(payload)

@router.get("/order/{order_id}")
def buscar_pedido(order_id: int):
    return get_order(order_id)

@router.delete("/order/{order_id}", status_code=204)
def deletar_pedido(order_id: int):
    return delete_order(order_id)

@router.get("/inventory")
def buscar_inventario():
    return list_inventory()