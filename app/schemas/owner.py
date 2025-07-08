from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OwnerCreate(BaseModel):
    nome: str = Field(..., example="Universidade Federal do Pará")


class OwnerResponse(OwnerCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)
