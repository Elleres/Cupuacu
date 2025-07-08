from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from const.enum import UserStatusType, UserType


class UserResponse(BaseModel):
    id: UUID
    name: str = Field(..., examples=["John Doe", "Joao Fernando"])
    email: str = Field(..., examples=["exemplo@gmail.com"])
    username: str = Field(..., examples=["john_doe"])
    status: UserStatusType
    type: UserType

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str = Field(..., examples=["John Doe", "Joao Fernando"])
    email: str = Field(..., examples=["exemplo@gmail.com"])
    password: str
    username: str = Field(..., examples=["john_doe"])
    type: UserType = Field(..., examples=[UserType.gerente_laboratorio])

class UserCreateAdmin(UserCreate):
    status: UserStatusType

class UserLogin(BaseModel):
    username: str
    password: str
