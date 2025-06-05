from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connector import get_db
from schemas.token import Token
from schemas.user import UserCreate, UserLogin, UserResponse

from repositories.user_repositories import create_user
from services.auth_service import authenticate_user, hash_password, get_current_user
from utils.exceptions import integrity_error_database
from services.auth_service import oauth2_scheme

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    hashed_password = await hash_password(user.password)
    user.password = hashed_password

    try:
        user = await create_user(db, user)
    except IntegrityError as e:
        await integrity_error_database(e)

    return user

@router.post("/token", response_model=Token)
async def create_token_endpoint(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)
):
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    token = await authenticate_user(db, user_login)
    return token

@router.get("/me", response_model=UserResponse)
async def read_users_me(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    current_user = await get_current_user(db, token)

    return current_user
