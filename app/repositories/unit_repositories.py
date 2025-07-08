from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.unit import Unit
from schemas.unit import UnitCreate


async def create_unit(
        db: AsyncSession,
        unit_create: UnitCreate,
):
    db_unit = Unit(**unit_create.model_dump())

    db.add(db_unit)

    await db.commit()

    await db.refresh(db_unit)

    return db_unit.model_dump()

async def get_unit(
        db: AsyncSession,
        unit_id: UUID,
):
    db_unit = await db.get(Unit, unit_id)

    if not db_unit:
        return None

    return Unit(**db_unit.model_dump())


async def delete_unit(
        db: AsyncSession,
        unit_id: UUID
):
    db_unit = await db.get(Unit, unit_id)

    if not db_unit:
        return None

    await db.delete(db_unit)
    await db.commit()

    return 1