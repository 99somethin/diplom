from fastapi import Body

from pydantic import Field, BaseModel

from typing import Union, Annotated, Optional

from app.schemas.employer import EmployerBase
from app.schemas.candidate import CandidateBase
from app.schemas.user_profiles import (
    UserEmployerSchema,
    UserCandidateSchema,
    UserCandidateUpdateSchema,
    UserEmployerUpdateSchema,
)

ProfileUnion = Annotated[
    Union[EmployerBase, CandidateBase], Field(discriminator="role")
]

UserProfileSchema = Annotated[
    Union[UserEmployerSchema, UserCandidateSchema], Field(discriminator="role")
]

UserProfileUpdateSchema = Annotated[
    Union[UserEmployerUpdateSchema, UserCandidateUpdateSchema],
    Field(discriminator="role"),
]
