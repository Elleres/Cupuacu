import re

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


async def integrity_error_database(
        error: IntegrityError
):
    error_msg = str(error.orig)

    pattern = r"\([^()]*\)"
    error_details = re.search(pattern, error_msg).group()

    if "unique constraint" in error_msg:
        defined_status = 400
        message = "Unique constraint violada"
    elif "check constraint" in error_msg:
        defined_status = 422
        message = "Check constraint violada"
    elif "foreign key constraint" in error_msg:
        defined_status = 400
        message = "Foreign key constraint violada"
    else:
        defined_status = 500
        message = "Erro nao documentado"

    detail_dic = {
        "msg": message,
        "loc": error_details,
    }

    raise HTTPException(status_code=defined_status, detail=detail_dic)