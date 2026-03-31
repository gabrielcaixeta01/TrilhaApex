from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class CategoryCreate(BaseModel):
    name: str = Field(...)


class CategoryUpdate(BaseModel):
    name: str = Field(...)


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(...)


class TagUpdate(BaseModel):
    name: str = Field(...)


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(...)
    firstName: str | None = Field(None)
    lastName: str | None = Field(None)
    email: str | None = Field(None)
    password: str = Field(..., min_length=8)
    phone: str | None = Field(None)
    user_active: bool = Field(default=True)
    role: Literal["admin", "user", "viewer"] = Field(default="user")


class UserUpdate(BaseModel):
    username: str | None = Field(None)
    firstName: str | None = Field(None)
    lastName: str | None = Field(None)
    email: str | None = Field(None)
    password: str | None = Field(None, min_length=8)
    phone: str | None = Field(None)
    user_active: bool | None = Field(None)
    role: Literal["admin", "user", "viewer"] | None = Field(None)


class UserResponse(BaseModel):
    id: int
    username: str
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    phone: str | None = None
    user_active: bool = True
    role: Literal["admin", "user", "viewer"] = "user"

    class Config:
        from_attributes = True


class PetCreate(BaseModel):
    name: str = Field(...)
    photoUrls: str | None = Field(None)
    status: PetStatus = Field(default=PetStatus.available)
    category_id: int = Field(...)
    owner_id: int | None = Field(None)
    tag_ids: list[int] = Field(default_factory=list)


class PetUpdate(BaseModel):
    name: str | None = Field(None)
    photoUrls: str | None = Field(None)
    status: PetStatus | None = Field(None)
    category_id: int | None = Field(None)
    owner_id: int | None = Field(None)
    tag_ids: list[int] | None = Field(None)


class PetSummary(BaseModel):
    id: int
    name: str
    photoUrls: str | None = None
    status: PetStatus
    category_id: int
    owner_id: int | None = None

    class Config:
        from_attributes = True


class PetResponse(BaseModel):
    id: int
    name: str
    photoUrls: str | None = None
    status: PetStatus
    category_id: int
    owner_id: int | None = None
    category: CategoryResponse | None = None
    tags: list[TagResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    petId: int = Field(...)
    quantity: int = Field(default=1)
    shipDate: datetime | None = Field(default=None)
    status: str = Field(default="placed")
    complete: bool = Field(default=False)
    owner_id: int | None = Field(None)


class OrderUpdate(BaseModel):
    petId: int | None = Field(None)
    quantity: int | None = Field(None)
    shipDate: datetime | None = Field(None)
    status: str | None = Field(None)
    complete: bool | None = Field(None)
    owner_id: int | None = Field(None)


class OrderResponse(BaseModel):
    id: int
    petId: int
    quantity: int = 1
    shipDate: datetime | None = None
    status: str = "placed"
    complete: bool = False
    owner_id: int
    pet: PetSummary | None = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    session: int


class MessageResponse(BaseModel):
    message: str