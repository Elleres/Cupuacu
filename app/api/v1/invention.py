from uuid import UUID

from fastapi import APIRouter, Depends, Response, UploadFile, File, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.invention import InventionResponse, InventionCreate
from repositories.invention_repositories import create_invention, get_invention, delete_invention
from schemas.user import UserResponse
from services.auth_service import get_current_user
from services.storage import upload_object, delete_object
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found

router = APIRouter(tags=["CRUD - invention"])

BUCKET_NAME = "user-images"

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

@router.get("/invention")
async def get_invention_by_id(
        invention_id: UUID,
        db: AsyncSession = Depends(get_db)
):
    """
    Busca o a invenção pelo ID

    **Parâmetros**
    - invention_id: ID do objetivo invention que será utilizado para buscar no banco.

    **Retorna**
    - `InventionResponse`: Objeto contendo os dados da invenção criada.

    """
    invention = await get_invention(db, invention_id)

    if not invention:
        await instance_not_found("invention")

    return InventionResponse.model_validate(invention)

@router.delete("/invention")
async def delete_invention_endpoint(
        invention_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    resultado = await delete_invention(db, invention_id)

    if not resultado:
        await instance_not_found()

    if resultado == 1:
        return Response(status_code=HTTP_204_NO_CONTENT)

@router.post("/invention/image")
async def upload_invention_image(
        file: UploadFile = File(...),
):
    content = await file.read()

    try:
        await upload_object(BUCKET_NAME, file.filename, content, file.content_type)
        url = f"http://localhost:9000/{BUCKET_NAME}/{file.filename}"
        return {"url": url}
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/invention/image")
async def delete_invention_image(
        invention_id: str,
):
    try:
        await delete_object(BUCKET_NAME, str(invention_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))