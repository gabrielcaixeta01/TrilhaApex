"""
Router para operações de Orders (CRUD)
Endpoints documentados automaticamente no Swagger
"""
from datetime import datetime
from fastapi import APIRouter
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
    quantity: int,
    shipDate: datetime | None = None,
    status: str = "placed",
    complete: bool = False
) -> dict:
    """
    Criar um novo pedido
    
    - **order_id**: ID único do pedido
    - **petId**: ID do pet
    - **quantity**: Quantidade
    - **status**: Status do pedido (placed, approved, delivered)
    """
    return create_order(
        order_id=order_id,
        petId=petId,
        quantity=quantity,
        shipDate=shipDate,
        status=status,
        complete=complete
    )


@router.get("/order/{order_id}", response_model=dict)
def buscar_pedido(order_id: int) -> dict:
    """
    Buscar um pedido específico por ID
    
    - **order_id**: ID do pedido
    """
    return get_order(order_id)


@router.delete("/order/{order_id}", status_code=204)
def deletar_pedido(order_id: int) -> None:
    """
    Deletar um pedido
    
    - **order_id**: ID do pedido a deletar
    """
    delete_order(order_id)


@router.get("/inventory", response_model=dict)
def buscar_inventario() -> dict:
    """
    Listar inventário (quantidade de pets por status)
    """
    return list_inventory()