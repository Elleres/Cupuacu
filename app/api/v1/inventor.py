from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.inventor import InventorResponse, InventorCreate
from repositories.inventor_repositories import create_inventor, get_inventor, delete_inventor
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - inventor"])


@router.post("/inventor", response_model=None)
async def create_inventor_endpoint(
    inventor: InventorCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo inventor no sistema.

    **Requer permissões de administrador**

    **Parameters**:
    - `inventor (InventorCreate)`: Dados do inventor (nome, e-mail).

    **Returns**:
    - `InventorResponse`: Objeto contendo os dados do inventor criado.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para criar inventores.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        inventor = await create_inventor(db, inventor)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventorResponse.model_validate(inventor)


@router.get("/inventor")
async def get_inventor_by_id(
    inventor_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca um inventor pelo seu ID.

    **Parameters**:
    - `inventor_id (UUID)`: ID do inventor a ser buscado.

    **Returns**:
    - `InventorResponse`: Objeto contendo os dados do inventor encontrado.

    **Raises**:
    - `HTTPException` com status 404 caso o inventor não seja encontrado.
    """
    inventor = await get_inventor(db, inventor_id)

    if not inventor:
        await instance_not_found("inventor")

    return InventorResponse.model_validate(inventor)


@router.delete("/inventor")
async def delete_inventor_endpoint(
    inventor_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Remove um inventor do sistema a partir do seu ID.

    **Requer permissões de administrador**

    **Parameters**:
    - `inventor_id (UUID)`: ID do inventor a ser removido.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para deletar inventores.
    - `HTTPException` com status 404 caso o inventor não seja encontrado.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_inventor(db, inventor_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
