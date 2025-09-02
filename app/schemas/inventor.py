from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from const.enum import InventionType, InventionStatusType


class InventorCreate(BaseModel):

    nome: str = Field(..., example="John Doe")
    email: str = Field(..., example="example@exmail.com")



class InventorResponse(InventorCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)


class InventorFilters(BaseModel):
    start: int = 0
    limit: int = 20
    inventor_id: Optional[UUID]
    inventor_nome: Optional[List[str]]
    inventor_email: Optional[List[str]]