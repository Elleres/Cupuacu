from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship



class InventionOwner(SQLModel, table=True):
    __tablename__ = "invention_owner"


    id_owner: UUID = Field(default_factory=uuid4, primary_key=True, foreign_key="owner.id")
    id_invention: UUID = Field(default_factory=uuid4, primary_key=True, foreign_key="invention.id")


    owner: "Owner" = Relationship(back_populates="inventions")
    invention: "Invention" = Relationship(back_populates="owners")