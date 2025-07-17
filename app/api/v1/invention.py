import os
from uuid import UUID

from fastapi import APIRouter, Depends, Response, UploadFile, File, HTTPException, Form
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from const.enum import UserType
from db.db_connector import get_db
from schemas.invention import InventionResponse, InventionCreate
from repositories.invention_repositories import create_invention, get_invention, delete_invention
from schemas.user import UserResponse
from services.auth_service import get_current_user
from services.storage import upload_object, delete_object, list_objects_with_prefix
from utils.exceptions import integrity_error_database, unauthorized, instance_not_found, exceeded_limit_size
from utils.regex_utils import get_file_extension

router = APIRouter(tags=["CRUD - invention"])

BUCKET_NAME = "user-images"
MAX_IMAGE_PER_INVENTION = 10
MINIO_URL = os.getenv("MINIO_URL")

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
        invention_id: UUID = Form(...),
        file: UploadFile = File(...),
        current_user: UserResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if current_user.type != UserType.admin:
        await unauthorized()

    invention_db = await get_invention(db, invention_id)
    if not invention_db:
        await instance_not_found("invention")

    content = await file.read()
    formato = get_file_extension(file.filename)

    curr_objects = await list_objects_with_prefix(BUCKET_NAME, str(invention_id))
    indice_imagem = len(curr_objects) + 1

    minio_file_name = f"{invention_id}_{indice_imagem}.{formato}"

    if indice_imagem > MAX_IMAGE_PER_INVENTION:
        await exceeded_limit_size(MAX_IMAGE_PER_INVENTION)

    await upload_object(BUCKET_NAME, minio_file_name, content, file.content_type)

    return {"url": f"{MINIO_URL}/{BUCKET_NAME}/{minio_file_name}"}


@router.get("/invention/image", tags=["vitrine"])
async def get_invention_image(
        invention_id: UUID,
):
    objetos = await list_objects_with_prefix(BUCKET_NAME, str(invention_id))

    return objetos

@router.delete("/invention/image", status_code=HTTP_204_NO_CONTENT)
async def delete_invention_image(
        file_name: str,
        current_user: UserResponse = Depends(get_current_user),
):
    if current_user.type != UserType.admin:
        await unauthorized()

    result = await delete_object(BUCKET_NAME, str(file_name))

    if not result["success"]:
        await instance_not_found("file_name")