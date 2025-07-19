from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.unit import UnitResponse, UnitCreate
from repositories.unit_repositories import create_unit, get_unit, delete_unit
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - unit"])


@router.post("/unit", response_model=None)
async def create_unit_endpoint(
    unit: UnitCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria uma nova unidade no sistema.

    **Requer permissões de administrador**

    **Parameters**:
    - `unit (UnitCreate)`: Dados da unidade a ser criada (nome, sigla, tipo).

    **Returns**:
    - `UnitResponse`: Objeto contendo os dados da unidade criada.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para criar (somente admins).
    - `HTTPException` com status 400 em caso de erro de integridade no banco de dados.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        unit = await create_unit(db, unit)
    except IntegrityError as e:
        await integrity_error_database(e)

    return UnitResponse.model_validate(unit)


@router.get("/unit")
async def get_unit_by_id(
    unit_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca uma unidade pelo seu ID.

    **Parameters**:
    - `unit_id (UUID)`: ID da unidade a ser buscada.

    **Returns**:
    - `UnitResponse`: Objeto contendo os dados da unidade encontrada.

    **Raises**:
    - `HTTPException` com status 404 caso a unidade não seja encontrada.
    """
    unit = await get_unit(db, unit_id)

    if not unit:
        await instance_not_found("unit")

    return UnitResponse.model_validate(unit)


@router.delete("/unit")
async def delete_unit_endpoint(
    unit_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Remove uma unidade pelo seu ID.

    **Requer permissões de administrador**

    **Parameters**:
    - `unit_id (UUID)`: ID da unidade a ser removida.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para deletar (somente admins).
    - `HTTPException` com status 404 caso a unidade não seja encontrada.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_unit(db, unit_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
