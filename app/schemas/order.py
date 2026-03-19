from pydantic import BaseModel, Field

class OrderSchema(BaseModel):
    id: int = Field(..., gt=0, description="ID do pedido")
    petId: int = Field(..., gt=0, description="ID do pet")
    quantity: int = Field(..., gt=0, description="Quantidade de pets")
    shipDate: str = Field(..., description="Data de envio no formato ISO 8601")
    status: str = Field(..., pattern="(?i)^(placed|approved|delivered)$", description="Status do pedido")
    complete: bool = Field(default=False, description="Indica se o pedido está completo")

class InventoryResponseSchema(BaseModel):
    status: str = Field(..., description="Status do inventário")
    quantity: int = Field(..., gt=0, description="Quantidade disponível")

class OrderCreateSchema(OrderSchema):
	pass


class OrderResponseSchema(OrderSchema):
	id: int = Field(..., gt=0)
