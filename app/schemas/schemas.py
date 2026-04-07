from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Store(BaseModel):
    id: int
    name: str
    cnpj: str
    phone: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: Optional[str] = None
    role: str
    phone: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    client_type: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    job_title: Optional[str] = None
    hired_at: Optional[date] = None
    store_id: Optional[int] = None
    user_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class Tag(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class Pet(BaseModel):
    id: int
    name: str
    species: Optional[str] = None
    breed: Optional[str] = None
    sex: Optional[str] = None
    birth_date: Optional[date] = None
    size: Optional[str] = None
    weight: Optional[Decimal] = None
    health_notes: Optional[str] = None
    status: PetStatus
    category_id: int
    owner_id: int
    active: bool = True

    class Config:
        from_attributes = True


class Service(BaseModel):
    id: int
    service_type: str
    description: Optional[str] = None
    service_at: datetime
    status: str
    price: Optional[Decimal] = None
    discount: Optional[Decimal] = Decimal("0")
    payment_type: Optional[str] = None
    observations: Optional[str] = None
    store_id: int
    pet_id: int
    client_id: int
    worker_id: int

    class Config:
        from_attributes = True
