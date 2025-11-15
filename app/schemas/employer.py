from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class EmployerBackGround(BaseModel):
    company_name: str
    company_description: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EmployerBase(EmployerBackGround):
    role: Literal["employer"] = Field(default="employer", frozen=True)


class EmployerBaseOut(EmployerBackGround):
    pass


class EmployerCreateSchema(EmployerBackGround):
    pass


class EmployerUpdateSchema(EmployerBackGround):
    company_name: Optional[str] = None
