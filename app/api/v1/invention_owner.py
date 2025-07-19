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

router = APIRouter(tags=["CRUD - invention_owner"])


@router.post("/invention_owner", response_model=None)
async def create_invention_owner_endpoint(
    invention_owner: InventionOwnerCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo vínculo entre uma invenção e um proprietário.

    **Requer permissões de administrador**

    **Parameters**:
    - `invention_owner (InventionOwnerCreate)`: Dados da relação (id_invention, id_owner).

    **Returns**:
    - `InventionOwnerResponse`: Objeto contendo os dados da relação criada.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        invention_owner = await create_invention_owner(db, invention_owner)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventionOwnerResponse.model_validate(invention_owner)


@router.get("/invention_owner")
async def get_invention_owner_by_id(
    id_invention: UUID,
    id_owner: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca o vínculo entre invenção e proprietário pelo ID.

    **Parameters**:
    - `id_invention (UUID)`: ID da invenção.
    - `id_owner (UUID)`: ID do proprietário.

    **Returns**:
    - `InventionOwnerResponse`: Objeto contendo os dados da relação.

    **Raises**:
    - `HTTPException` com status 404 caso a relação não seja encontrada.
    """
    invention_owner = await get_invention_owner(db, id_invention, id_owner)

    if not invention_owner:
        await instance_not_found("invention_owner")

    return InventionOwnerResponse.model_validate(invention_owner)


@router.delete("/invention_owner")
async def delete_invention_owner_endpoint(
    id_invention: UUID,
    id_owner: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Remove o vínculo entre invenção e proprietário.

    **Requer permissões de administrador**

    **Parameters**:
    - `id_invention (UUID)`: ID da invenção.
    - `id_owner (UUID)`: ID do proprietário.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 404 caso a relação não seja encontrada.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_invention_owner(db, id_invention, id_owner)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
