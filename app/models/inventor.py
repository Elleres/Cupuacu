from typing import List
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


class Inventor(SQLModel, table=True):
    __tablename__ = "inventor"


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)


    inventions: List["InventorInvention"] = Relationship(back_populates="inventor")