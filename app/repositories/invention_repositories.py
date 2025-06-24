from sqlalchemy.ext.asyncio import AsyncSession

from models.invention import Invention
from schemas.invention import InventionCreate, InventionResponse


async def create_invention(
        db: AsyncSession,
        invention_create: InventionCreate,
):
    db_user = Invention(**invention_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()
