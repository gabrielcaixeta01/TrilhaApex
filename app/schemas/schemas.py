from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from enum import Enum

from pydantic import BaseModel, Field


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Store(BaseModel):
    id: int
    name: str
    cnpj: str
    phone: str
    email: str
    cep: str
    city: str
    state: str
    address: str
    neighborhood: str
    number: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class StoreCreate(BaseModel):
    name: str
    cnpj: str
    phone: str
    email: str
    cep: str
    city: str
    state: str
    address: str
    neighborhood: str
    number: str
    active: bool = True


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    cep: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    number: Optional[str] = None
    active: Optional[bool] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    phone: str
    role: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    role: str = "cliente"
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    active: bool = True
    is_superuser: bool = False
    client_type: Optional[str] = None
    client_cep: Optional[str] = None
    client_state: Optional[str] = None
    client_city: Optional[str] = None
    matricula: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[Decimal] = None
    hired_at: Optional[date] = None
    store_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    client_type: Optional[str] = None
    client_cep: Optional[str] = None
    client_state: Optional[str] = None
    client_city: Optional[str] = None
    matricula: Optional[str] = None
    job_title: Optional[str] = None
    salary: Optional[Decimal] = None
    hired_at: Optional[date] = None
    store_id: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Client(BaseModel):
    user_id: int
    client_type: str
    cep: str
    state: str
    city: str

    class Config:
        from_attributes = True


class Employee(BaseModel):
    user_id: int
    matricula: str
    job_title: str
    salary: Decimal
    hired_at: date
    store_id: int

    class Config:
        from_attributes = True


class Category(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Tag(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Pet(BaseModel):
    id: int
    name: str
    breed: Optional[str] = None
    sex: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[Decimal] = None
    health_notes: Optional[str] = None
    category_id: int
    owner_id: int

    class Config:
        from_attributes = True


class PetCreate(BaseModel):
    name: str
    breed: Optional[str] = None
    sex: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[Decimal] = None
    health_notes: Optional[str] = None
    category_id: int
    owner_id: int


class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    sex: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[Decimal] = None
    health_notes: Optional[str] = None
    category_id: Optional[int] = None
    owner_id: Optional[int] = None


class Service(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal

    class Config:
        from_attributes = True


class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None


class Appointment(BaseModel):
    id: int
    value_final: Decimal
    service_at: datetime
    payment_type: str
    status: str
    online: bool = False
    observations: Optional[str] = None
    store_id: int
    client_id: int
    worker_id: int
    pet_id: int
    items: List['AppointmentService'] = []

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    value_final: Decimal
    service_at: Optional[datetime] = None
    payment_type: str
    status: str
    online: bool = False
    observations: Optional[str] = None
    store_id: int
    client_id: int
    worker_id: int
    pet_id: int


class AppointmentUpdate(BaseModel):
    value_final: Optional[Decimal] = None
    service_at: Optional[datetime] = None
    payment_type: Optional[str] = None
    status: Optional[str] = None
    online: Optional[bool] = None
    observations: Optional[str] = None
    store_id: Optional[int] = None
    client_id: Optional[int] = None
    worker_id: Optional[int] = None
    pet_id: Optional[int] = None


class AppointmentService(BaseModel):
    appointment_id: int
    service_id: int
    charged_value: Decimal
    order_date: datetime
    delivery_date: Optional[datetime] = None
    observations: Optional[str] = None

    class Config:
        from_attributes = True


class AppointmentServiceCreate(BaseModel):
    appointment_id: int
    service_id: int
    charged_value: Decimal
    order_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    observations: Optional[str] = None


class AppointmentServiceUpdate(BaseModel):
    charged_value: Optional[Decimal] = None
    order_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    observations: Optional[str] = None
