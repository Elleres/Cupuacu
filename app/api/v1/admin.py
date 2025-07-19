from typing import Union, List
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from const.enum import UserType, UserStatusType, TicketStatusType
from db.db_connector import get_db
from repositories.laboratory_repositories import create_laboratory
from repositories.ticket_repositories import get_tickets
from schemas.laboratory import LaboratoryCreateAdmin, LaboratoryResponse
from schemas.ticket import TicketResponse
from schemas.user import UserResponse, UserCreateAdmin

from repositories.user_repositories import create_user
from services.auth_service import hash_password, get_current_user
from utils.exceptions import integrity_error_database, unauthorized

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Create new user"
)
async def create_user_endpoint(
    user: UserCreateAdmin,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Cria um novo usuário, permitindo usar as permissões de administrador para alterar o status do usuário.

    **Requer permissões de administrador**

    **Parameters**:
    - `user (UserCreateAdmin)`: Dados do usuário que será criado.

    **Returns**:
    - `UserResponse`: O recém criado usuário.

    **Raises**:
    - `HTTPException` com status 200 caso tudo ocorra corretamente.
    - `HTTPException` com status 401 caso o usuário não possua a permissão para fazer a criação.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
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
    """
    Cria um novo laboratório no sistema.

    **Requer permissões de administrador**

    **Parameters**:
    - `laboratory (LaboratoryCreateAdmin)`: Dados do laboratório a ser criado.

    **Returns**:
    - `LaboratoryResponse`: O laboratório recém criado.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua a permissão para fazer a criação.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
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
    """
    Lista os tickets com filtros opcionais por status e tecnologia alvo.

    **Requer permissões de administrador**

    **Parameters**:
    - `start (int)`: Offset para paginação. Padrão: 0.
    - `limit (int)`: Número máximo de resultados. Padrão: 20.
    - `id_tecnologia_alvo (UUID | None)`: ID da tecnologia alvo (opcional).
    - `status (List[TicketStatusType] | None)`: Lista de status dos tickets (opcional).

    **Returns**:
    - `List[TicketResponse]`: Lista de tickets filtrados.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua a permissão para fazer a consulta.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    result = await get_tickets(db, status, id_tecnologia_alvo, start, limit)
    return [TicketResponse.model_validate(x) for x in result]
