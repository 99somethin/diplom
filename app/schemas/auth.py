from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.user import UserRole

from typing import Optional


class RegisterInSchema(BaseModel):
    email: EmailStr = Field(max_length=55)
    password: str = Field(exclude=True)
    full_name: Optional[str] = Field(max_length=100)
    role: UserRole = Field(default=None)

    model_config = ConfigDict()


class RegisterOutSchema(BaseModel):
    email: EmailStr = Field(max_length=55)
    role: UserRole = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class LoginInSchema(BaseModel):
    email: EmailStr
    password: str


class LoginOutSchema(BaseModel):
    email: EmailStr = Field(max_length=55)
    full_name: Optional[str] = Field(max_length=100)

    model_config = ConfigDict(from_attributes=True)
