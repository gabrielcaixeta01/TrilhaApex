from http.client import HTTPException

from scripts.script2 import Order
from app.schemas.models import OrderSchema


def create_order(payload: OrderSchema):
    order = Order(
        order_id=payload.order_id,
        pet_id=payload.petId,
        quantity=payload.quantity,
        ship_date=payload.shipDate,
        status=payload.status,
        complete=payload.complete,
    )
    result = order.criar()

    if not result:
        raise HTTPException(status_code=400, detail="Failed to create order")
    
    return result


def get_order(order_id):
    result = Order.buscar(order_id)

    if not result:
        raise HTTPException(status_code=404, detail="Order not found")

    return result

def delete_order(order_id):
    result = Order.deletar(order_id)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to delete order")

    return result
    

def list_inventory():
    inventory = Order.inventario()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    
    return inventory
