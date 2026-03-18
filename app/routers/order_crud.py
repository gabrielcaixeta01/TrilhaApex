from fastapi import APIRouter, Response
from app.schemas.order import OrderCreateSchema,  OrderResponseSchema
from app.services.order_service import (
    create_order,
    get_order,
    delete_order,
    list_inventory,
)

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/{order_id}", response_model=OrderResponseSchema, status_code=201)
def criar_pedido(order_id: int, payload: OrderCreateSchema):
    return create_order(order_id, payload)

@router.get("/{order_id}", response_model=OrderResponseSchema)
def buscar_pedido(order_id: int):
    return get_order(order_id)

@router.delete("/{order_id}", status_code=204)
def deletar_pedido(order_id: int):
    delete_order(order_id)
    return Response(status_code=204)

@router.get("/inventory")
def buscar_inventario():
    return list_inventory()