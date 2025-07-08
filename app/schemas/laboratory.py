from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from const.enum import LaboratoryStatusType


class LaboratoryCreate(BaseModel):
    id_unit: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    id_user: Optional[UUID] = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890cdddef")
    nome: str = Field(..., example="Laboratório de Bioinformática e Computação de Alto Desempenho")
    sigla: str = Field(..., example="LABioCAD")
    resumo: str = Field(..., example="Texto explicando o passado e o presente do laboratório.", max_length=3000)
    condicao_de_uso: str = Field(..., example="Texto explicando condições para o uso do laboratório.", max_length=3000)

class LaboratoryCreateAdmin(LaboratoryCreate):
    status: LaboratoryStatusType = Field(default=LaboratoryStatusType.accepted)

class LaboratoryResponse(LaboratoryCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)
