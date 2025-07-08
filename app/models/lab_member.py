from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


class LabMember(SQLModel, table=True):
    __tablename__ = "lab_member"


    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_laboratory: UUID = Field(primary_key=True, foreign_key="laboratory.id")
    nome: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)
    telefone: str = Field(nullable=False, max_length=20)

    laboratory: "Laboratory" = Relationship(back_populates="lab_members")