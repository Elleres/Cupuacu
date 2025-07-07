from typing import List
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship


class Owner(SQLModel, table=True):
    __tablename__ = "owner"


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(nullable=False, max_length=255, unique=True)


    inventions: List["InventionOwner"] = Relationship(back_populates="owner")