from typing import List, Optional
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

class UnitFilters(BaseModel):
    start: int = 0
    limit: int = 20
    unit_id: Optional[UUID]
    unit_name: Optional[List[str]]
    unit_sigla: Optional[List[str]]
    unit_tipo: Optional[List[UnitType]]