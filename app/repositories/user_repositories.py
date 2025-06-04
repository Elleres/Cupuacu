from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserResponse
from models.user import User
from services.auth_service import pwd_context


async def create_user(
        db: AsyncSession,
        user: UserCreate
):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    db_user = User(**user.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return UserResponse.model_validate(db_user.model_dump())