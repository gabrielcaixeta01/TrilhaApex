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
    return order


def get_order(order_id):
    result = Order.buscar(order_id)

    return result

def delete_order(order_id):
    order = Order(order_id, None, None, None, None, None)
    result = order.deletar(order_id)

    return result
    

def get_inventory():
    inventory = Order.inventario()
    return inventory
