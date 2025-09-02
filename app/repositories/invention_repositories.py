from uuid import UUID

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.invention import Invention
from models.invention_owner import InventionOwner
from models.inventor import Inventor
from models.inventor_invention import InventorInvention
from models.owner import Owner
from models.unit import Unit
from schemas.invention import InventionCreate, InventionFilters


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
        invention_filters: InventionFilters
):
    FILTER_MAP = {
        "unit_id": Invention.id_unit,
        "unit_name": Unit.nome,
        "unit_sigla": Unit.sigla,
        "unit_tipo": Unit.tipo,
        "inv_titulo": Invention.titulo,
        "inv_situacao": Invention.situacao,
        "inv_trl": Invention.trl,
        "inv_tipo": Invention.type,
        "inventor_name": Inventor.nome,
        "owner_name": Owner.nome,
    }

    # 1. Subquery com joins e filtros
    subq = (
        select(Invention.id)
        .join(Unit)
        .outerjoin(InventorInvention)
        .outerjoin(Inventor)
        .outerjoin(InventionOwner)
        .outerjoin(Owner)
    )

    for field_name, column in FILTER_MAP.items():
        value = getattr(invention_filters, field_name)
        if value is not None:
            if isinstance(value, list):
                subq = subq.where(column.in_(value))
            else:
                subq = subq.where(column == value)

    subq = subq.offset(invention_filters.start).limit(invention_filters.limit)
    result = await db.execute(subq)
    ids = [row[0] for row in result.all()]

    # 2. Select real com selectinload
    stmt = (
        select(Invention)
        .where(Invention.id.in_(ids))
        .options(
            selectinload(Invention.unit),
            selectinload(Invention.inventors).selectinload(InventorInvention.inventor),
            selectinload(Invention.owners).selectinload(InventionOwner.owner),
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()
