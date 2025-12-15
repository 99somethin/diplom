from pydantic import BaseModel, Field, ConfigDict

from typing import Literal

from app.schemas.candidate import CandidateBaseOut, CandidateUpdateSchema
from app.schemas.employer import EmployerBaseOut, EmployerUpdateSchema
from app.schemas.user import UserBaseOutSchema, UserUpdateSchema


class UserProfileBaseSchema(BaseModel):
    user: UserBaseOutSchema
    model_config = ConfigDict(from_attributes=True)

class UserProfileUpdateSchema(BaseModel):
    user: UserUpdateSchema
    model_config = ConfigDict(from_attributes=True)


class UserEmployerSchema(UserProfileBaseSchema):
    employer: EmployerBaseOut
    role: Literal["employer"] = Field(frozen=True, default="employer")


class UserCandidateSchema(UserProfileBaseSchema):
    candidate: CandidateBaseOut
    role: Literal["candidate"] = Field(frozen=True, default="candidate")


class UserEmployerUpdateSchema(UserProfileUpdateSchema):
    employer: EmployerUpdateSchema
    role: Literal["employer"] = Field(frozen=True, default="employer")


class UserCandidateUpdateSchema(UserProfileUpdateSchema):
    candidate: CandidateUpdateSchema
    role: Literal["candidate"] = Field(frozen=True, default="candidate")
