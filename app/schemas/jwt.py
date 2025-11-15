from pydantic import BaseModel, ConfigDict

class JWTCreateSchema(BaseModel):
    sub: str
    name: str
    role: str 

    model_config = ConfigDict(from_attributes=True)