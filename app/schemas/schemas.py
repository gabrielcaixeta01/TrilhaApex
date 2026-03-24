from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Nome da categoria")

class Category(CategoryCreate):
    id: int = Field(..., description="ID único da categoria")
    
    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str = Field(..., description="Nome da tag")

class Tag(TagCreate):
    id: int = Field(..., description="ID único da tag")
    
    class Config:
        from_attributes = True


class PetCreate(BaseModel):
    name: str = Field(..., description="Nome do pet")
    photoUrls: Optional[str] = Field(None, description="URL de foto do pet")
    status: str = Field(default="available", description="Status do pet (available, pending, sold)")
    category_id: Optional[int] = Field(None, description="ID da categoria do pet")

class Pet(PetCreate):
    id: int = Field(..., description="ID único do pet")
    category: Optional[Category] = Field(None, description="Categoria do pet")
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    petId: int = Field(..., description="ID do pet")
    quantity: Optional[int] = Field(None, description="Quantidade")
    shipDate: Optional[datetime] = Field(None, description="Data de envio")
    status: str = Field(default="placed", description="Status do pedido (placed, approved, delivered)")
    complete: bool = Field(default=False, description="Indica se o pedido está completo")

class Order(OrderCreate):
    id: int = Field(..., description="ID único do pedido")
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., description="Nome de usuário único")
    firstName: Optional[str] = Field(None, description="Primeiro nome")
    lastName: Optional[str] = Field(None, description="Último nome")
    email: Optional[str] = Field(None, description="Email do usuário")
    password: str = Field(..., description="Senha do usuário")
    phone: Optional[str] = Field(None, description="Número de telefone")
    userStatus: int = Field(default=1, description="Status do usuário (0=inativo, 1=ativo)")

class User(UserCreate):
    id: int = Field(..., description="ID único do usuário")
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int = Field(..., description="ID único do usuário")
    username: str = Field(..., description="Nome de usuário")
    firstName: Optional[str] = Field(None, description="Primeiro nome")
    lastName: Optional[str] = Field(None, description="Último nome")
    email: Optional[str] = Field(None, description="Email")
    phone: Optional[str] = Field(None, description="Telefone")
    userStatus: int = Field(default=1, description="Status do usuário")
    
    class Config:
        from_attributes = True
