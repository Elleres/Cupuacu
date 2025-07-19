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

router = APIRouter(tags=["CRUD - owner"])


@router.post("/owner", response_model=None)
async def create_owner_endpoint(
    owner: OwnerCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo proprietário no sistema.

    **Requer permissões de administrador**

    **Parameters**:
    - `owner (OwnerCreate)`: Dados do proprietário a ser criado.

    **Returns**:
    - `OwnerResponse`: Objeto contendo os dados do proprietário criado.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para criar.
    - `HTTPException` com status 400 caso ocorra erro de integridade no banco de dados.
    """
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
    """
    Busca um proprietário pelo seu ID.

    **Parameters**:
    - `owner_id (UUID)`: ID do proprietário a ser buscado.

    **Returns**:
    - `OwnerResponse`: Objeto contendo os dados do proprietário encontrado.

    **Raises**:
    - `HTTPException` com status 404 caso o proprietário não seja encontrado.
    """
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
    """
    Remove um proprietário do sistema pelo seu ID.

    **Requer permissões de administrador**

    **Parameters**:
    - `owner_id (UUID)`: ID do proprietário a ser removido.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão para deletar.
    - `HTTPException` com status 404 caso o proprietário não seja encontrado.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_owner(db, owner_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
