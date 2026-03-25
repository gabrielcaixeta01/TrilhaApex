from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from typing import Literal
from enum import Enum


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"

class CategoryCreate(BaseModel):
    name: str = Field(...)

class Category(CategoryCreate):
    id: int = Field(...)
    
    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(...)

class Tag(TagCreate):
    id: int = Field(...)
    
    class Config:
        from_attributes = True


class PetCreate(BaseModel):
    name: str = Field(...)
    photoUrls: Optional[str] = Field(None)
    status: PetStatus = Field(...)
    category_id: Optional[int] = Field(None)
    owner_id: Optional[int] = Field(None)

class Pet(PetCreate):
    id: int = Field(...)
    category: Optional[Category] = Field(None)
    owner: Optional[User] = Field(None)

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    petId: int = Field(...)
    quantity: int = Field(default=1)
    shipDate: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="placed")
    complete: bool = Field(default=False)

class Order(OrderCreate):
    id: int = Field(...)
    owner: Optional[User] = Field(None)
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(...)
    firstName: Optional[str] = Field(None)
    lastName: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    password: str = Field(..., min_length=8)
    phone: Optional[str] = Field(None)
    user_active: bool = Field(default=True)
    role: Literal["admin", "user", "viewer"] = Field(default="user")

class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class User(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    firstName: Optional[str] = Field(None)
    lastName: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    user_active: bool = Field(default=True)
    role: Literal["admin", "user", "viewer"] = Field(default="user")
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(default="bearer")