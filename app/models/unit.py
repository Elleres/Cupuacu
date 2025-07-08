from datetime import date
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlmodel import Field, SQLModel, Relationship

from const.enum import UnitType


class Unit(SQLModel, table=True):
    __tablename__ = "unit"

    __table_args__ = (
        UniqueConstraint("nome", "sigla", name="uq0_unit"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(nullable=False, max_length=255)
    sigla: str = Field(nullable=False, max_length=255)
    tipo: UnitType = Field(nullable=False, default=UnitType.faculdade)

    inventions: List["Invention"] = Relationship(back_populates="unit")
    laboratories: List["Laboratory"] = Relationship(back_populates="unit")