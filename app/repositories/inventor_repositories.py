from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.inventor import Inventor
from schemas.inventor import InventorCreate


async def create_inventor(
        db: AsyncSession,
        inventor_create: InventorCreate,
):
    db_user = Inventor(**inventor_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_inventor(
        db: AsyncSession,
        inventor_id: UUID,
):
    db_inventor = await db.get(Inventor, inventor_id)

    if not db_inventor:
        return None

    return Inventor(**db_inventor.model_dump())


async def delete_inventor(
        db: AsyncSession,
        inventor_id: UUID
):
    db_inventor = await db.get(Inventor, inventor_id)

    if not db_inventor:
        return None

    await db.delete(db_inventor)
    await db.commit()

    return 1