from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.owner import OwnerResponse, OwnerCreate
from repositories.owner_repositories import create_owner, get_owner, delete_owner
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["owner"])


@router.post("/owner", response_model=None)
async def create_owner_endpoint(
        owner: OwnerCreate,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        owner = await create_owner(db, owner)
    except IntegrityError as e:
        await integrity_error_database(e)

    return OwnerResponse.model_validate(owner)

@router.get("/owner")
async def get_owner_by_id(
        owner_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    owner = await get_owner(db, owner_id)

    if not owner:
        await instance_not_found("owner")

    return OwnerResponse.model_validate(owner)

@router.delete("/owner")
async def delete_owner_endpoint(
        owner_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_owner(db, owner_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)