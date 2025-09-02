from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.unit import Unit
from schemas.unit import UnitCreate, UnitFilters


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

async def get_units(
        db: AsyncSession,
        unit_filters: UnitFilters
):
    FILTER_MAP = {
        "unit_id": Unit.id,
        "unit_name": Unit.nome,
        "unit_sigla": Unit.sigla,
        "unit_tipo": Unit.tipo,
    }

    stmt = select(Unit)
    for field_name, column in FILTER_MAP.items():
        value = getattr(unit_filters, field_name)
        if value is not None:
            if isinstance(value, list):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)
    result = await db.execute(stmt)

    return result.scalars().all()