from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.invention_owner import InventionOwnerResponse, InventionOwnerCreate
from repositories.invention_owner_repositories import create_invention_owner, get_invention_owner, delete_invention_owner
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["invention_owner"])


@router.post("/invention_owner", response_model=None)
async def create_invention_owner_endpoint(
        invention_owner: InventionOwnerCreate,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        invention_owner = await create_invention_owner(db, invention_owner)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventionOwnerResponse.model_validate(invention_owner)

@router.get("/invention_owner")
async def get_invention_owner_by_id(
        invention_owner_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    invention_owner = await get_invention_owner(db, invention_owner_id)

    if not invention_owner:
        await instance_not_found("invention_owner")

    return InventionOwnerResponse.model_validate(invention_owner)

@router.delete("/invention_owner")
async def delete_invention_owner_endpoint(
        invention_owner_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_invention_owner(db, invention_owner_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)