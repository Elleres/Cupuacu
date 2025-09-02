from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.inventor import Inventor
from schemas.inventor import InventorCreate, InventorFilters


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


async def get_inventors(
        db: AsyncSession,
        inventor_filters: InventorFilters
):
    FILTER_MAP = {
        "inventor_id": Inventor.id,
        "inventor_nome": Inventor.nome,
        "inventor_email": Inventor.email
    }

    stmt = select(Inventor)

    for field_name, column in FILTER_MAP.items():
        value = getattr(inventor_filters, field_name)
        if value is not None:
            if isinstance(value, list):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)
    result = await db.execute(stmt)

    return result.scalars().all()