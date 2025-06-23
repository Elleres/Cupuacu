from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from const.enum import UserType, UserStatusType

class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=255)
    email: str = Field(nullable=False, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    status: UserStatusType = Field(nullable=False, default=UserStatusType.on_hold)
    type: UserType = Field(nullable=False)