from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    username: str


class UserLogin(BaseModel):
    username: str
    password: str
