from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from const.enum import UserType
from db.db_connector import get_db
from schemas.invention import InventionResponse, InventionCreate
from repositories.invention_repositories import create_invention
from schemas.user import UserResponse
from services.auth_service import get_current_user
from utils.exceptions import integrity_error_database, unauthorized

router = APIRouter(tags=["invention"])


@router.post("/invention", response_model=None)
async def create_invention_endpoint(
        invention: InventionCreate,
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Processa a requisição para criar um novo usuário.

    **Parâmetros:**
    - `invention`: Objeto InventionCreate contendo os dados de uma nova invenção (titulo, descricao, situacao, trl, type, data_submissao)

    **Retorna:**
    - `InventionResponse`: Objeto contendo os dados da invenção criada.

    **Levanta:**
    - `HTTPException` com status 401 caso o usuário não possua a permissão para fazer a criação.
    """
    # Somente admins podem criar invenções
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        invention = await create_invention(db, invention)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventionResponse.model_validate(invention)