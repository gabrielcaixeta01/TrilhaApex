"""
Service de Orders - Lógica de negócio para operações com pedidos
"""
from datetime import datetime
from fastapi import HTTPException
from scripts.script2 import Order


def _normalize_order_response(result: dict) -> dict:
    """Normalizar resposta do Order para ter order_id em vez de id"""
    if isinstance(result, dict) and "id" in result and "order_id" not in result:
        normalized = result.copy()
        normalized["order_id"] = normalized.pop("id")
        return normalized
    return result


def _is_external_error(result: dict) -> bool:
    """Verificar se há erro externo"""
    return isinstance(result, dict) and isinstance(result.get("code"), int) and result.get("code") >= 400


def create_order(
    order_id: int,
    petId: int,
    quantity: int,
    shipDate: datetime | None = None,
    status: str = "placed",
    complete: bool = False
) -> dict:
    """Criar um novo pedido"""
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
        
        if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
            detail = result.get("message", "Erro ao criar pedido") if isinstance(result, dict) else "Erro ao criar pedido"
            raise HTTPException(status_code=400, detail=detail)
        
        return _normalize_order_response(result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar pedido: {str(e)}")


def get_order(order_id: int) -> dict:
    """Obter um pedido por ID"""
    try:
        result = Order.buscar(order_id)
        
        if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        return _normalize_order_response(result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar pedido: {str(e)}")


def delete_order(order_id: int) -> None:
    """Deletar um pedido"""
    try:
        result = Order.deletar(order_id)
        
        if not result or _is_external_error(result) or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=400, detail="Erro ao deletar pedido")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pedido: {str(e)}")


def list_inventory() -> dict:
    """Listar inventário (quantidade de pets por status)"""
    try:
        inventory = Order.inventario()
        
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventário não encontrado")
        
        return inventory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar inventário: {str(e)}")
