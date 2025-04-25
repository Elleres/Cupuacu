from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "user"  # <-- adiciona isso
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)
