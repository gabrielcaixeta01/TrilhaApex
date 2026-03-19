from fastapi import HTTPException
from scripts.script2 import Order
from app.schemas.order import OrderCreateSchema

def build_order(order_id: int, payload: OrderCreateSchema) -> Order:
    order = Order(
        order_id=order_id,
        pet_id=payload.petId,
        quantity=payload.quantity,
        ship_date=payload.shipDate,
        status=payload.status,
        complete=payload.complete,
    )

    return order

def create_order(order_id: int, payload: OrderCreateSchema) -> dict:
    order = build_order(order_id, payload)
    result = order.criar()

    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="Retorno invalido da API externa ao criar pedido")

    if result.get("id") is not None:
        return result

    # A API Petstore pode responder com code/type/message em alguns cenarios.
    if result.get("code") == 200:
        return payload.model_dump()

    raise HTTPException(
        status_code=502,
        detail=f"Falha ao criar pedido na API externa: {result}",
    )

    

def get_order(order_id):
    result = Order.buscar(order_id)

    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")

    return result

def delete_order(order_id):
    order = Order(order_id, None, None, None, None, None)
    result = order.deletar(order_id)

    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    
def list_inventory():
    result = Order.inventario()

    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="Falha ao obter inventário da API externa")

    return result
