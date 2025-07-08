from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from const.enum import UnitType


class UnitCreate(BaseModel):

    nome: str = Field(..., example="Faculdade de Computação")
    sigla: str = Field(..., example="FACOMP")
    tipo: UnitType = Field(..., example=UnitType.faculdade)


class UnitResponse(UnitCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)
