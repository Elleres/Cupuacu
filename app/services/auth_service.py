import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connector import DatabaseConnector
from repositories.user_repositories import get_user_by_email, get_user_by_username
from schemas.token import TokenData, Token
from schemas.user import UserLogin, UserResponse
from utils.exceptions import instance_not_found, invalid_login

SECRET_KEY = os.getenv('SECRET_KEY', 'dev_example')
ALGORITHM = os.getenv('ALGORITHM', 'HS256') # HS256 should be changed in future
ACESS_TOKEN_EXPIRATION_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_acess_token(
        data: dict
):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({'exp': expire})
    token = Token(
        access_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),
        token_type="Bearer"
    )
    return token


async def get_current_user(
        db: AsyncSession,
        token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return UserResponse.model_validate(user)

async def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)

async def authenticate_user(
        db: AsyncSession,
        credentials: UserLogin,
):
    user = await get_user_by_username(db, credentials.username)
    if not user:
        await instance_not_found(
            "Username"
        )

    if pwd_context.verify(credentials.password, user.password):
        return await create_acess_token({"sub": credentials.username})
    else:
        await invalid_login()