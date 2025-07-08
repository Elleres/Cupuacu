from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from const.enum import TicketStatusType


class TicketCreateRequest(BaseModel):
    id_tecnologia_alvo: UUID = Field(..., example="c1b3c3d4-e5f6-7890-1234-567890cdddef")
    nome_do_projeto: str = Field(..., example="ENTRE - Ferramenta de modelagem de curriculos")
    status: TicketStatusType = TicketStatusType.open
    criado_em: datetime = datetime.now()
    atualizado_em: datetime = datetime.now()

class TicketCreate(TicketCreateRequest):
    id_user: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890cdddef")

class TicketResponse(TicketCreate):
    id: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")

    model_config = ConfigDict(from_attributes=True)
