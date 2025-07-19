from uuid import UUID

from fastapi import APIRouter, Depends, Response, UploadFile, File, Form
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.const import BUCKET_NAME
from const.enum import UserType
from db.db_connector import get_db
from schemas.invention import InventionResponse, InventionCreate
from repositories.invention_repositories import create_invention, get_invention, delete_invention
from schemas.user import UserResponse
from services.auth_service import get_current_user
from services.invention_image import upload_invention_image_logic
from utils.storage import delete_object, list_objects_with_prefix
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - invention"])


@router.post("/invention", response_model=None)
async def create_invention_endpoint(
    invention: InventionCreate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Cria uma nova invenção no sistema.

    **Requer permissões de administrador**

    **Parameters**:
    - `invention (InventionCreate)`: Dados da invenção (título, descrição, situação, TRL, tipo, data de submissão).

    **Returns**:
    - `InventionResponse`: Dados da invenção criada.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 400 caso ocorra um erro de integridade no banco de dados.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    try:
        invention = await create_invention(db, invention)
    except IntegrityError as e:
        await integrity_error_database(e)

    return InventionResponse.model_validate(invention)


@router.get("/invention")
async def get_invention_by_id(
    invention_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Busca uma invenção pelo seu ID.

    **Parameters**:
    - `invention_id (UUID)`: ID da invenção.

    **Returns**:
    - `InventionResponse`: Dados da invenção encontrada.

    **Raises**:
    - `HTTPException` com status 404 caso a invenção não seja encontrada.
    """
    invention = await get_invention(db, invention_id)

    if not invention:
        await instance_not_found("invention")

    return InventionResponse.model_validate(invention)


@router.delete("/invention", status_code=HTTP_204_NO_CONTENT)
async def delete_invention_endpoint(
    invention_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Deleta uma invenção pelo ID.

    **Requer permissões de administrador**

    **Parameters**:
    - `invention_id (UUID)`: ID da invenção a ser deletada.

    **Returns**:
    - `204 No Content`: Se a invenção foi removida com sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 404 caso a invenção não seja encontrada.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_invention(db, invention_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)


@router.post("/invention/image")
async def upload_invention_image_endpoint(
    invention_id: UUID = Form(...),
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Faz upload de uma imagem associada a uma invenção.

    **Requer permissões de administrador**

    **Parameters**:
    - `invention_id (UUID)`: ID da invenção.
    - `file (UploadFile)`: Arquivo de imagem a ser enviado.

    **Returns**:
    - `dict`: URL da imagem enviada.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 404 caso a invenção não seja encontrada.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    result = await upload_invention_image_logic(db, invention_id, file)
    return {"url": result}


@router.get("/invention/image", tags=["vitrine"])
async def get_invention_image(
    invention_id: UUID,
):
    """
    Lista as imagens associadas a uma invenção.

    **Parameters**:
    - `invention_id (UUID)`: ID da invenção.

    **Returns**:
    - `list[str]`: Lista de URLs das imagens encontradas.
    """
    objetos = await list_objects_with_prefix(BUCKET_NAME, str(invention_id))
    return objetos


@router.delete("/invention/image", status_code=HTTP_204_NO_CONTENT)
async def delete_invention_image_endpoint(
    file_name: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Remove uma imagem específica associada a uma invenção.

    **Requer permissões de administrador**

    **Parameters**:
    - `file_name (str)`: Nome do arquivo a ser removido.

    **Returns**:
    - `204 No Content`: Se a imagem foi removida com sucesso.

    **Raises**:
    - `HTTPException` com status 401 caso o usuário não possua permissão.
    - `HTTPException` com status 404 caso o arquivo não seja encontrado.
    """
    if current_user.type != UserType.admin:
        await unauthorized()

    result = await delete_object(BUCKET_NAME, str(file_name))

    if not result["success"]:
        await instance_not_found("file_name")
