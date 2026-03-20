from pydantic import BaseModel, Field
from typing import Literal


class CategorySchema(BaseModel):
	id: int = Field()
	name: str = Field()


class TagSchema(BaseModel):
	id: int = Field()
	name: str = Field()


class PetCreateSchema(BaseModel):
    category: CategorySchema
    photoUrls: list[str] = Field(default_factory=list)
    tags: list[TagSchema] = Field(default_factory=list)
    status: Literal["available", "pending", "sold"] = Field(default="available")


class PetUpdateSchema(BaseModel):
    category: CategorySchema
    name: str = Field(...)
    photoUrls: list[str] = Field(default_factory=list)
    tags: list[TagSchema] = Field(default_factory=list)
    status: Literal["available", "pending", "sold"] = Field(default="available")


class OrderSchema(BaseModel):
    order_id: int = Field()
    petId: int = Field()
    quantity: int = Field()
    shipDate: str = Field()
    status: str = Field(default="placed", pattern="(?i)^(placed|approved|delivered)$")
    complete: bool = Field(default=False)

class InventorySchema(BaseModel):
    status: str = Field()
    quantity: int = Field()


class UserSchema(BaseModel):
    id: int = Field()
    username: str = Field(...)
    firstName: str = Field()
    lastName: str = Field()
    email: str = Field()
    password: str = Field(...)
    phone: str = Field()
    userStatus: int = Field(default=0)

class UserCreateSchema(BaseModel):
    id: int = Field()
    firstName: str = Field()
    lastName: str = Field()
    email: str = Field()
    phone: str = Field()
    userStatus: int = Field(default=0)


class UserUpdateSchema(BaseModel):
    id: int = Field()
    firstName: str = Field()
    lastName: str = Field()
    email: str = Field()
    password: str = Field(...)
    phone: str = Field()
    userStatus: int = Field(default=0)
