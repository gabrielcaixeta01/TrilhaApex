from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class Category(BaseModel):
    id: int
    name: str


class Tag(BaseModel):
    id: int
    name: str


class Pet(BaseModel):
    id: int
    name: str
    photoUrls: list[str] | None = None
    status: Literal["available", "pending", "sold"] = "available"
    category: Category | None = None
    tags: list[Tag] | None = None


class Order(BaseModel):
    order_id: int
    petId: int
    quantity: int | None = None
    shipDate: datetime | None = None
    status: str = "placed"
    complete: bool = False


class User(BaseModel):
    id: int
    username: str
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    password: str
    phone: str | None = None
    userStatus: int = 0
