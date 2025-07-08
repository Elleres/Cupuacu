from datetime import date
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import Field, SQLModel, Relationship

from const.enum import LaboratoryStatusType


class Laboratory(SQLModel, table=True):
    __tablename__ = "laboratory"

    __table_args__ = (
        UniqueConstraint("nome", "sigla", name="uq0_laboratory"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_unit: UUID = Field(foreign_key="unit.id", nullable=False)
    id_user: UUID = Field(default=None, foreign_key="user.id")
    nome: str = Field(nullable=False, max_length=255)
    sigla: str = Field(nullable=False, max_length=255)
    resumo: str = Field(nullable=False, max_length=3000)
    condicao_de_uso: str = Field(nullable=False, max_length=3000)
    status: LaboratoryStatusType = Field(nullable=False, default="on_hold")

    unit: "Unit" = Relationship(back_populates="laboratories")
    user: "User" = Relationship(back_populates="laboratory")
    lab_members: List["LabMember"] = Relationship(back_populates="laboratory")