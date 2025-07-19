from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.inventor_invention import InventorInvention
from schemas.inventor_invention import InventorInventionCreate


async def create_inventor_invention(
        db: AsyncSession,
        inventor_invention_create: InventorInventionCreate,
):
    db_user = InventorInvention(**inventor_invention_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_inventor_invention(
        db: AsyncSession,
        inventor_id: UUID,
        invention_id: UUID
):
    db_inventor_invention = await db.get(InventorInvention, entity={
        "id_inventor": inventor_id,
        "id_invention": invention_id
    })

    if not db_inventor_invention:
        return None

    return InventorInvention(**db_inventor_invention.model_dump())


async def delete_inventor_invention(
        db: AsyncSession,
        inventor_id: UUID,
        invention_id: UUID
):
    db_inventor_invention = await db.get(InventorInvention, entity={
        "id_inventor": inventor_id,
        "id_invention": invention_id
    })

    if not db_inventor_invention:
        return None

    await db.delete(db_inventor_invention)
    await db.commit()

    return 1