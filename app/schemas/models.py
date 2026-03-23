"""
Esquemas/Modelos de dados usando Type Hints nativos do Python
FastAPI gera automaticamente a documentação Swagger com base nesses tipos
"""
from typing import Literal
from datetime import datetime


# ============ CATEGORY ============
class Category:
    """Categoria de pets"""
    id: int
    name: str
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


# ============ TAG ============
class Tag:
    """Tags/etiquetas para categorizar pets"""
    id: int
    name: str
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


# ============ PET ============
class Pet:
    """Animal de estimação"""
    id: int
    name: str
    photoUrls: list[str]
    status: Literal["available", "pending", "sold"]
    category: Category | None
    tags: list[Tag]
    
    def __init__(
        self,
        id: int,
        name: str,
        photoUrls: list[str] | None = None,
        status: Literal["available", "pending", "sold"] = "available",
        category: Category | None = None,
        tags: list[Tag] | None = None
    ):
        self.id = id
        self.name = name
        self.photoUrls = photoUrls or []
        self.status = status
        self.category = category
        self.tags = tags or []


# ============ ORDER ============
class Order:
    """Pedido de compra"""
    order_id: int
    petId: int
    quantity: int
    shipDate: datetime | None
    status: str
    complete: bool
    
    def __init__(
        self,
        order_id: int,
        petId: int,
        quantity: int,
        shipDate: datetime | None = None,
        status: str = "placed",
        complete: bool = False
    ):
        self.order_id = order_id
        self.petId = petId
        self.quantity = quantity
        self.shipDate = shipDate
        self.status = status
        self.complete = complete


# ============ USER ============
class User:
    """Usuário do sistema"""
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str | None
    userStatus: int
    
    def __init__(
        self,
        id: int,
        username: str,
        firstName: str,
        lastName: str,
        email: str,
        password: str,
        phone: str | None = None,
        userStatus: int = 0
    ):
        self.id = id
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.userStatus = userStatus
