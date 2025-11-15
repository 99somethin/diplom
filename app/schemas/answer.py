from typing import Optional
from pydantic import BaseModel, ConfigDict


class AnswerBase(BaseModel):
    answear_link: Optional[str] = None
    feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AnswerOut(AnswerBase):
    review_feedback: Optional[str] = None


class AnswerCreateIn(AnswerBase):
    pass


class AnswerCreateOut(AnswerBase):
    pass


class AnswerUpdateIn(AnswerBase):
    pass

class AnswerUpdateOut(AnswerBase):
    pass

class Feedback(BaseModel):
    review_feedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
