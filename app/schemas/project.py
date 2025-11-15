from datetime import date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


class ProjectBackGround(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=4000)

    model_config = ConfigDict(from_attributes=True)


class ProjectMinOut(ProjectBackGround):
    pass


class ProjectBase(ProjectBackGround):
    requirements: Optional[List[str]] = Field(max_length=100, default=None)
    deadline: Optional[date] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class ProjectFullOut(ProjectBase):
    pass


class ProjectCreateIn(ProjectBase):
    pass

class ProjectCreateOut(ProjectBase):
    pass


class ProjectUpdateIn(ProjectBase):
    pass


class ProjectUpdateOut(ProjectBase):
    pass