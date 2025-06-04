from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connector import get_db
from schemas.user import UserCreate

from repositories.user_repositories import create_user
from utils.exceptions import integrity_error_database

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        user = await create_user(db, user)
    except IntegrityError as e:
        await integrity_error_database(e)

    return user