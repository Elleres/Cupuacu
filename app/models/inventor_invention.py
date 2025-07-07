from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship



class InventorInvention(SQLModel, table=True):
    __tablename__ = "inventor_invention"


    id_inventor: UUID = Field(default_factory=uuid4, primary_key=True, foreign_key="inventor.id")
    id_invention: UUID = Field(default_factory=uuid4, primary_key=True, foreign_key="invention.id")


    inventor: "Inventor" = Relationship(back_populates="inventions")
    invention: "Invention" = Relationship(back_populates="inventors")