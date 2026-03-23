from datetime import datetime
from fastapi import HTTPException
from scripts.script2 import Order


def create_order(order_id: int, petId: int, quantity: int | None = None, shipDate: datetime | None = None, status: str = "placed", complete: bool = False):
    try:
        order = Order(
            order_id=order_id,
            pet_id=petId,
            quantity=quantity,
            ship_date=shipDate.isoformat() if shipDate else None,
            status=status,
            complete=complete,
        )
        result = order.criar()
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao criar pedido")
        return result
    except HTTPException:
        raise

def get_order(order_id: int):
    try:
        result = Order.buscar(order_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        if isinstance(result, dict) and result.get("code") == 1:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return result
    except HTTPException:
        raise

def delete_order(order_id: int):
    try:
        result = Order.deletar(order_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        if isinstance(result, dict) and result.get("code") == 1:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return result
    except HTTPException:
        raise

def list_inventory():
    try:
        inventory = Order.inventario()
        
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventário não encontrado")
        
        return inventory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar inventário: {str(e)}")
