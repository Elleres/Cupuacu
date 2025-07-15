from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.invention import Invention
from models.invention_owner import InventionOwner
from models.inventor_invention import InventorInvention
from schemas.invention import InventionCreate


async def create_invention(
        db: AsyncSession,
        invention_create: InventionCreate,
):
    db_user = Invention(**invention_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()


async def get_invention(
        db: AsyncSession,
        invention_id: UUID
):
    db_invention = await db.get(Invention, invention_id)

    if not db_invention:
        return None

    return db_invention

async def delete_invention(
        db: AsyncSession,
        invention_id: UUID
):
    db_invention = await db.get(Invention, invention_id)

    if not db_invention:
        return None

    await db.delete(db_invention)
    await db.commit()

    return 1

async def get_inventions(
        db: AsyncSession,
        start: int,
        limit: int,
):
    stmt = select(Invention).options(
        selectinload(Invention.unit),
        selectinload(Invention.inventors).selectinload(InventorInvention.inventor),
        selectinload(Invention.owners).selectinload(InventionOwner.owner),
    ).offset(start).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()