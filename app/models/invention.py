from datetime import date
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import Field, SQLModel

from const.enum import InventionType, InventionStatusType


class Invention(SQLModel, table=True):
    __tablename__ = "invention"

    __table_args__ = (
        # Trl precisa estar entre 1 e 9
        CheckConstraint("trl > 0 and trl < 10", name="ch0_invention_trl"),
        UniqueConstraint("titulo", "type", name="uq0_invention")
    )


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    titulo: str = Field(nullable=False, max_length=255)
    descricao: str = Field(nullable=False, max_length=2000)
    situacao: InventionStatusType = Field(nullable=False)
    trl: int = Field(nullable=False, default=1)
    type: InventionType = Field(nullable=False)
    data_submissao: date = Field(nullable=False)

    # Unidade, titulares e inventores será uma tabela a parte.