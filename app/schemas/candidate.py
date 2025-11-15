from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field


class CandidateBackGround(BaseModel):
    bio: Optional[str] = None
    resume_link: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CandidateBase(CandidateBackGround):
    role: Literal["candidate"] = Field(default="candidate", frozen=True)


class CandidateBaseOut(CandidateBackGround):
    pass


class CandidateCreateSchema(CandidateBackGround):
    pass


class CandidateUpdateSchema(CandidateBackGround):
    pass
