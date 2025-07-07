from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship

from const.enum import TicketStatusType


class Ticket(SQLModel, table=True):
    __tablename__ = "ticket"


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_user: UUID = Field(primary_key=True, foreign_key="user.id")
    id_tecnologia_alvo: UUID = Field(primary_key=True) # Essa coluna é necessário fazer uma verificação na camada de aplicação
    nome_do_projeto: str = Field(nullable=False, max_length=255, unique=True)
    status: TicketStatusType = Field(nullable=False, max_length=255, default=TicketStatusType.open)
    criado_em: datetime = Field(nullable=False, default_factory=datetime.now)
    atualizado_em: datetime = Field(nullable=False, default_factory=datetime.now)


    user: "User" = Relationship(back_populates="tickets")