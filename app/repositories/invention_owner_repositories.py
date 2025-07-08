from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.invention_owner import InventionOwner
from schemas.invention_owner import InventionOwnerCreate


async def create_invention_owner(
        db: AsyncSession,
        invention_owner_create: InventionOwnerCreate,
):
    db_user = InventionOwner(**invention_owner_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_invention_owner(
        db: AsyncSession,
        invention_owner_id: UUID,
):
    db_invention_owner = await db.get(InventionOwner, invention_owner_id)

    if not db_invention_owner:
        return None

    return InventionOwner(**db_invention_owner.model_dump())


async def delete_invention_owner(
        db: AsyncSession,
        invention_owner_id: UUID
):
    db_invention_owner = await db.get(InventionOwner, invention_owner_id)

    if not db_invention_owner:
        return None

    await db.delete(db_invention_owner)
    await db.commit()

    return 1