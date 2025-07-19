from uuid import UUID

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.laboratory import LaboratoryResponse, LaboratoryCreate, LaboratoryCreateAdmin
from repositories.laboratory_repositories import create_laboratory, get_laboratory, delete_laboratory
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - laboratory"])


@router.post("/laboratory", response_model=None)
async def create_laboratory_endpoint(
    laboratory: LaboratoryCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria um novo laboratório no sistema.

    **Requer permissões de administrador ou gerente de laboratório**

    **Parameters**:
    - `laboratory (LaboratoryCreate)`: Dados do laboratório a ser criado.

    **Returns**:
    - `LaboratoryResponse`: Objeto contendo os dados do laboratório criado.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 400 caso ocorra erro de integridade no banco de dados.
    """
    if current_user.type not in [UserType.admin, UserType.gerente_laboratorio]:
        await unauthorized()

    try:
        laboratory = await create_laboratory(db, laboratory)
    except IntegrityError as e:
        await integrity_error_database(e)

    return LaboratoryResponse.model_validate(laboratory)


@router.get("/laboratory")
async def get_laboratory_by_id(
    laboratory_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca um laboratório pelo seu ID.

    **Parameters**:
    - `laboratory_id (UUID)`: ID do laboratório a ser buscado.

    **Returns**:
    - `LaboratoryResponse`: Objeto contendo os dados do laboratório encontrado.

    **Raises**:
    - `HTTPException` com status 404 caso o laboratório não seja encontrado.
    """
    laboratory = await get_laboratory(db, laboratory_id)

    if not laboratory:
        await instance_not_found("laboratory")

    return LaboratoryResponse.model_validate(laboratory)


@router.delete("/laboratory")
async def delete_laboratory_endpoint(
    laboratory_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Remove um laboratório do sistema pelo seu ID.

    **Requer permissões de administrador ou gerente de laboratório**

    **Parameters**:
    - `laboratory_id (UUID)`: ID do laboratório a ser removido.

    **Returns**:
    - `204 No Content`: Em caso de sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 404 caso o laboratório não seja encontrado.
    """
    if current_user.type not in [UserType.admin, UserType.gerente_laboratorio]:
        await unauthorized()

    resultado = await delete_laboratory(db, laboratory_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)
