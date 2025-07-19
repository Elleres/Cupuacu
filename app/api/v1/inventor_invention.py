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

router = APIRouter(tags=["CRUD - inventor_invention"])


@router.post("/inventor_invention", response_model=None)
async def create_inventor_invention_endpoint(
    inventor_invention: InventorInventionCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo vínculo entre inventor e invenção.

    **Requer permissões de administrador**

    **Parameters**:
    - `inventor_invention (InventorInventionCreate)`: Dados da relação entre inventor e invenção.

    **Returns**:
    - `InventorInventionResponse`: Objeto contendo os dados da relação criada.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para criar.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        inventor_invention = await create_inventor_invention(db, inventor_invention)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventorInventionResponse.model_validate(inventor_invention)


@router.get("/inventor_invention")
async def get_inventor_invention_by_id(
    inventor_id: UUID,
    invention_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca o vínculo entre inventor e invenção pelo inventor_id e invention_id.

    **Parameters**:
    - `inventor_id (UUID)`: ID do inventor.
    - `invention_id (UUID)`: ID da invenção.

    **Returns**:
    - `InventorInventionResponse`: Objeto contendo os dados da relação encontrada.

    **Raises**:
    - `HTTPException` com status 404 caso a relação não seja encontrada.
    """
    inventor_invention = await get_inventor_invention(db, inventor_id, invention_id)

    if not inventor_invention:
        await instance_not_found("inventor_invention")

    return InventorInventionResponse.model_validate(inventor_invention)


@router.delete("/inventor_invention")
async def delete_inventor_invention_endpoint(
    inventor_id: UUID,
    invention_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Remove o vínculo entre inventor e invenção.

    **Requer permissões de administrador**

    **Parameters**:
    - `inventor_id (UUID)`: ID do inventor.
    - `invention_id (UUID)`: ID da invenção.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para excluir.
    - `HTTPException` com status 404 caso a relação não seja encontrada.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_inventor_invention(db, inventor_id, invention_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
