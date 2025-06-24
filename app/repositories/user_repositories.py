from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserResponse
from models.user import User


async def create_user(
        db: AsyncSession,
        user: UserCreate
):
    db_user = User(**user.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()


async def get_user_by_email(
        db: AsyncSession,
        email: str
):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().one_or_none()

async def get_user_by_username(
        db: AsyncSession,
        username: str
):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalars().one_or_none()