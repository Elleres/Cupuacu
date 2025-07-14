from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.ticket import TicketResponse, TicketCreate, TicketCreateRequest
from repositories.ticket_repositories import create_ticket, get_ticket, delete_ticket
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - ticket"])


@router.post("/ticket", response_model=None)
async def create_ticket_endpoint(
        ticket: TicketCreateRequest,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()
    ticket = TicketCreate(**{"id_user": current_user.id,**ticket.model_dump()})
    try:
        ticket = await create_ticket(db, ticket)
    except IntegrityError as e:
        await integrity_error_database(e)

    return TicketResponse.model_validate(ticket)

@router.get("/ticket")
async def get_ticket_by_id_endpoint(
        ticket_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    ticket = await get_ticket(db, ticket_id)

    if not ticket:
        await instance_not_found("ticket")

    return TicketResponse.model_validate(ticket)

@router.delete("/ticket")
async def delete_ticket_endpoint(
        ticket_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_ticket(db, ticket_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)