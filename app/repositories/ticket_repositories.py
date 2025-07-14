from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

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