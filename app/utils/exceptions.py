import re
import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


async def integrity_error_database(
        error: IntegrityError
):
    error_msg = str(error.orig)

    pattern = r"\([^()]*\)"
    error_details = re.search(pattern, error_msg).group()

    if "unique constraint" in error_msg:
        defined_status = status.HTTP_400_BAD_REQUEST
        message = "Unique constraint violada"
    elif "check constraint" in error_msg:
        defined_status = status.HTTP_400_BAD_REQUEST
        message = "Check constraint violada"
    elif "foreign key constraint" in error_msg:
        defined_status = status.HTTP_400_BAD_REQUEST
        message = "Foreign key constraint violada"
    else:
        defined_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "Erro nao documentado"
    logging.error(error_msg)
    detail_dic = {
        "msg": message,
        "loc": error_details,
    }

    raise HTTPException(status_code=defined_status, detail=detail_dic)

async def instance_not_found(
        context: str
):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "msg": "Instance not found",
            "loc": context,
        }
    )

async def invalid_login():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "msg": "Invalid credentials",
            "loc": "Credentials",
        }
    )