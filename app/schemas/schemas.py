from typing import Literal
from datetime import datetime


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Tag:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Pet:
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


class Order:
    def __init__(
        self,
        order_id: int,
        petId: int,
        quantity: int | None = None,
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


class User:
    def __init__( 
        self,
        id: int,
        username: str,
        password: str, 
        firstName: str | None = None, 
        lastName: str | None = None,
        email: str | None = None, 
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
