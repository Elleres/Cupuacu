from typing import Union, List
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from const.enum import UserType, UserStatusType, TicketStatusType
from db.db_connector import get_db
from repositories.laboratory_repositories import create_laboratory
from repositories.ticket_repositories import get_tickets
from schemas.laboratory import LaboratoryCreateAdmin, LaboratoryResponse
from schemas.ticket import TicketResponse
from schemas.user import  UserResponse, UserCreateAdmin

from repositories.user_repositories import create_user
from services.auth_service import hash_password, get_current_user
from utils.exceptions import integrity_error_database, unauthorized

router = APIRouter(prefix="/admin" ,tags=["admin"])


@router.post("/users")
async def create_user_endpoint(
        user: UserCreateAdmin,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    hashed_password = await hash_password(user.password)
    user.password = hashed_password
    user.status = UserStatusType.active

    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        user = await create_user(db, user)
    except IntegrityError as e:
        await integrity_error_database(e)

    return UserResponse.model_validate(user)



@router.post("/laboratory", response_model=None)
async def create_laboratory_endpoint(
        laboratory: LaboratoryCreateAdmin,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        laboratory = await create_laboratory(db, laboratory)
    except IntegrityError as e:
        await integrity_error_database(e)

    return LaboratoryResponse.model_validate(laboratory)

@router.get("/tickets")
async def get_all_tickets_endpoint(
        start: int = 0,
        limit: int = 20,
        id_tecnologia_alvo: Union[UUID | None] = None,
        status: Union[List[TicketStatusType] | None] = Query(None),
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    result = await get_tickets(db, status, id_tecnologia_alvo, start, limit)

    result = [TicketResponse.model_validate(x) for x in result]

    return result
