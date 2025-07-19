from typing import List, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from const.enum import TicketStatusType
from models.ticket import Ticket
from schemas.ticket import TicketCreate


async def create_ticket(
        db: AsyncSession,
        ticket_create: TicketCreate,
):
    db_user = Ticket(**ticket_create.model_dump())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user.model_dump()

async def get_ticket(
        db: AsyncSession,
        ticket_id: UUID,
):
    db_ticket = await db.get(Ticket, ident=ticket_id)
    if not db_ticket:
        return None

    return Ticket(**db_ticket.model_dump())


async def delete_ticket(
        db: AsyncSession,
        ticket_id: UUID
):
    db_ticket = await db.get(Ticket, ticket_id)

    if not db_ticket:
        return None

    await db.delete(db_ticket)
    await db.commit()

    return 1

async def get_tickets(
        db: AsyncSession,
        status: Union[List[TicketStatusType] | None] = None,
        id_tecnologia_alvo: Union[UUID | None] = None,
        start: int = 0,
        limit: int = 20
):
    query = select(Ticket)

    if id_tecnologia_alvo:
        query = query.where(Ticket.id_tecnologia_alvo == id_tecnologia_alvo)

    if status:
        query = query.where(Ticket.status.in_(status))

    query = query.offset(start).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()
