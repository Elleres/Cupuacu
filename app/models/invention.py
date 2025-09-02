from datetime import date
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import Field, SQLModel, Relationship

from const.enum import InventionType, InventionStatusType


class Invention(SQLModel, table=True):
    __tablename__ = "invention"

    __table_args__ = (
        # Trl precisa estar entre 1 e 9
        CheckConstraint("trl > 0 and trl < 10", name="ch0_invention_trl"),
        UniqueConstraint("titulo", "type", name="uq0_invention")
    )


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_unit: UUID = Field(foreign_key="unit.id", nullable=False)
    titulo: str = Field(nullable=False, max_length=255)
    descricao: str = Field(nullable=False, max_length=2000)
    situacao: InventionStatusType = Field(nullable=False)
    trl: int = Field(nullable=False, default=1)
    type: InventionType = Field(nullable=False)
    data_submissao: date = Field(nullable=False)

    unit: "Unit" = Relationship(back_populates="inventions")
    owners: List["InventionOwner"] = Relationship(back_populates="invention")
    inventors: List["InventorInvention"] = Relationship(back_populates="invention")