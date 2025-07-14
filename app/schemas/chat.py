from uuid import UUID

from pydantic import BaseModel, Field


class WSConnectionRequest(BaseModel):
    ticket_id: UUID = Field(..., description="ID do ticket que o usuário quer acessar o chat")
    token: str = Field(..., description="Token de acesso do usuário")