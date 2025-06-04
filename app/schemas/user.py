from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
