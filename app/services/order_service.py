from fastapi import HTTPException

from scripts.script2 import Order
from app.schemas.models import OrderSchema


def _normalize_order_response(result):
    if isinstance(result, dict) and "id" in result and "order_id" not in result:
        normalized = result.copy()
        normalized["order_id"] = normalized.pop("id")
        return normalized
    return result


def _is_external_error(result):
    return isinstance(result, dict) and isinstance(result.get("code"), int) and result.get("code") >= 400


def create_order(payload: OrderSchema):
    order = Order(
        order_id=payload.order_id,
        pet_id=payload.petId,
        quantity=payload.quantity,
        ship_date=payload.shipDate.isoformat(),
        status=payload.status,
        complete=payload.complete,
    )
    result = order.criar()

    if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
        detail = result.get("message", "Failed to create order") if isinstance(result, dict) else "Failed to create order"
        raise HTTPException(status_code=400, detail=detail)
    
    return _normalize_order_response(result)


def get_order(order_id):
    result = Order.buscar(order_id)

    if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
        raise HTTPException(status_code=404, detail="Order not found")

    return _normalize_order_response(result)

def delete_order(order_id):
    result = Order.deletar(order_id)

    if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
        raise HTTPException(status_code=400, detail="Failed to delete order")

    return result
    

def list_inventory():
    inventory = Order.inventario()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    return inventory
