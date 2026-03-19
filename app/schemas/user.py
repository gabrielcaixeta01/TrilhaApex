from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    phone: str = Field(...)
    userStatus: int = Field(...)

