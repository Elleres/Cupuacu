from datetime import date
from typing import Optional, List
from uuid import UUID, uuid4

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from const.enum import InventionType, InventionStatusType, UnitType


class InventionCreate(BaseModel):

    id_unit: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    titulo: str = Field(..., example="Cadeira de Rodas Infantil Acessível")
    descricao: str = Field(
        ...,
        example=(
            "Trata-se de uma cadeira de rodas infantil, que atende crianças com deficiência e "
            "que é capaz de proporcionar mais independência em seu dia a dia. É de fabricação "
            "acessível, pode ser reutilizada, seu material é de baixo custo (MDF) e impressão 3D, "
            "apenas as rodinhas de silicone são compradas por fora. Todo o trabalho é feito no "
            "próprio laboratório do Ipê lab. A Mariana, aluna da faculdade de Design de Moda (FAV/UFG), "
            "também participa criando as almofadas e os estofados. É uma tecnologia que proporciona "
            "acessibilidade para crianças."
        )
    )
    situacao: InventionStatusType = Field(..., example=InventionStatusType.concedido_registrado)
    trl: int = Field(..., example=5, description="Nível de Maturidade Tecnológica (1 a 9)")
    type: InventionType = Field(..., example=InventionType.patente_de_invencao)
    data_submissao: date = Field(..., example=date.today().isoformat(),
                                 description="Data de submissão no formato YYYY-MM-DD")  # Exemplo no formato ISO 8601


class InventionResponse(InventionCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)

class InventionFilters(BaseModel):
    start: int = 0
    limit: int = 20
    unit_id: Optional[UUID]
    unit_name: Optional[List[str]]
    unit_sigla: Optional[List[str]]
    unit_tipo: Optional[List[UnitType]]
    inv_titulo: Optional[str]
    inv_situacao: Optional[List[InventionStatusType]]
    inv_trl: Optional[List[int]]
    inv_tipo: Optional[List[InventionType]]
    inventor_name: Optional[List[str]]
    owner_name: Optional[List[str]]

    @field_validator("inv_trl")
    def check_trl(cls, v):
        if v == None:
            return v
        for i in v:
            if i < 1 or i > 9:
                raise ValueError("inv_trl deve estar entre 1 e 9")
        return v
