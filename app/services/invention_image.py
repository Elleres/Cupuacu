from uuid import UUID

from fastapi import UploadFile

from const.const import BUCKET_NAME, MAX_IMAGE_PER_INVENTION, MINIO_URL
from repositories.invention_repositories import get_invention
from utils.storage import list_objects_with_prefix, upload_object
from utils.exceptions import instance_not_found, exceeded_limit_size
from utils.regex_utils import get_file_extension, get_max_index_filename_list


async def upload_invention_image_logic(db, invention_id: UUID, file: UploadFile) -> str:

    invention_db = await get_invention(db, invention_id)
    if not invention_db:
        await instance_not_found("invention")

    content = await file.read()
    formato = get_file_extension(file.filename)

    curr_objects = await list_objects_with_prefix(BUCKET_NAME, str(invention_id))

    if len(curr_objects) >= MAX_IMAGE_PER_INVENTION:
        await exceeded_limit_size(MAX_IMAGE_PER_INVENTION)

    max_index = get_max_index_filename_list(curr_objects)

    minio_file_name = f"{invention_id}_{max_index + 1}.{formato}"
    await upload_object(BUCKET_NAME, minio_file_name, content, file.content_type)
    return f"{MINIO_URL}/{BUCKET_NAME}/{minio_file_name}"