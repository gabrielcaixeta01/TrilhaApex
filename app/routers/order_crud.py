from fastapi import APIRouter, Response
from app.schemas.order import OrderCreateSchema,  OrderResponseSchema
from app.services.order_service import (
    create_order,
    get_order,
    delete_order,
    list_inventory,
)

router = APIRouter(prefix="/store", tags=["Store"])

@router.post("/order", response_model=OrderResponseSchema, status_code=201)
def criar_pedido(payload: OrderCreateSchema):
    return create_order(payload.id, payload)

@router.get("/order/{order_id}", response_model=OrderResponseSchema)
def buscar_pedido(order_id: int):
    return get_order(order_id)

@router.delete("/order/{order_id}", status_code=204)
def deletar_pedido(order_id: int):
    delete_order(order_id)
    return Response(status_code=204)

@router.get("/inventory")
def buscar_inventario():
    return list_inventory()