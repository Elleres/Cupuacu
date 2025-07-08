from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.owner import Owner
from schemas.owner import OwnerCreate


async def create_owner(
        db: AsyncSession,
        owner_create: OwnerCreate,
):
    db_user = Owner(**owner_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_owner(
        db: AsyncSession,
        owner_id: UUID,
):
    db_owner = await db.get(Owner, owner_id)

    if not db_owner:
        return None

    return Owner(**db_owner.model_dump())


async def delete_owner(
        db: AsyncSession,
        owner_id: UUID
):
    db_owner = await db.get(Owner, owner_id)

    if not db_owner:
        return None

    await db.delete(db_owner)
    await db.commit()

    return 1