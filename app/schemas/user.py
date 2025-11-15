from pydantic import BaseModel, EmailStr, ConfigDict, Field

from typing import Optional

from app.models.user import UserRole


class UserBackGroundSchema(BaseModel):
    email: EmailStr = Field(max_length=55)
    full_name: Optional[str] = Field(max_length=100)

    model_config = ConfigDict(from_attributes=True)


class UserBaseSchema(UserBackGroundSchema):
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=None)
    profile_completed: bool = Field()

class UserBaseOutSchema(UserBackGroundSchema):
    is_active: bool = Field(default=True)
    profile_completed: bool = Field()


class UserCreateSchema(UserBackGroundSchema):
    password: str
    role: UserRole


class UserUpdateSchema(UserBackGroundSchema):
    email: Optional[EmailStr] = Field(max_length=55, default=None)
    full_name: Optional[str] = Field(max_length=100, default=None) 

