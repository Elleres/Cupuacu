from typing import Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.laboratory import Laboratory
from schemas.laboratory import LaboratoryCreate, LaboratoryCreateAdmin


async def create_laboratory(
        db: AsyncSession,
        laboratory_create: Union[LaboratoryCreate, LaboratoryCreateAdmin],
):
    db_user = Laboratory(**laboratory_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_laboratory(
        db: AsyncSession,
        laboratory_id: UUID,
):
    db_laboratory = await db.get(Laboratory, laboratory_id)

    if not db_laboratory:
        return None

    return Laboratory(**db_laboratory.model_dump())


async def delete_laboratory(
        db: AsyncSession,
        laboratory_id: UUID
):
    db_laboratory = await db.get(Laboratory, laboratory_id)

    if not db_laboratory:
        return None

    await db.delete(db_laboratory)
    await db.commit()

    return 1