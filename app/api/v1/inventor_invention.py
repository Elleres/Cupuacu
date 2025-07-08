from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.inventor_invention import InventorInventionResponse, InventorInventionCreate
from repositories.inventor_invention_repositories import create_inventor_invention, get_inventor_invention, delete_inventor_invention
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["inventor_invention"])


@router.post("/inventor_invention", response_model=None)
async def create_inventor_invention_endpoint(
        inventor_invention: InventorInventionCreate,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        inventor_invention = await create_inventor_invention(db, inventor_invention)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventorInventionResponse.model_validate(inventor_invention)

@router.get("/inventor_invention")
async def get_inventor_invention_by_id(
        inventor_invention_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    inventor_invention = await get_inventor_invention(db, inventor_invention_id)

    if not inventor_invention:
        await instance_not_found("inventor_invention")

    return InventorInventionResponse.model_validate(inventor_invention)

@router.delete("/inventor_invention")
async def delete_inventor_invention_endpoint(
        inventor_invention_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_inventor_invention(db, inventor_invention_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)