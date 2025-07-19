from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from const.enum import UserType, UserStatusType
from db.db_connector import get_db
from schemas.token import Token
from schemas.user import UserCreate, UserLogin, UserResponse, UserCreateAdmin

from repositories.user_repositories import create_user
from services.auth_service import authenticate_user, hash_password, get_current_user
from utils.exceptions import integrity_error_database, unauthorized
from services.auth_service import oauth2_scheme

router = APIRouter(tags=["user"])


@router.post("/users")
async def create_user_endpoint(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Processa a requisição para criar um novo usuário.

    **Parameters**:
    - `user (UserCreate)`: Dados do novo usuário (nome, email, username, password e type).

    **Returns**:
    - `UserResponse`: Dados do usuário criado, excluindo a senha.

    **Raises**:
    - `HTTPException` com status 400 se os dados violarem restrições do banco.
    - `HTTPException` com status 401 se tentar criar usuário do tipo admin.
    """
    hashed_password = await hash_password(user.password)
    user.password = hashed_password

    if user.type == UserType.admin:
        await unauthorized()

    try:
        user = await create_user(db, user)
    except IntegrityError as e:
        await integrity_error_database(e)

    return UserResponse.model_validate(user)


@router.post("/token", response_model=Token)
async def create_token_endpoint(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    """
    Autentica um usuário e gera um token de acesso JWT.

    **Parameters**:
    - `form_data (OAuth2PasswordRequestForm)`: Dados de formulário com username e password.

    **Returns**:
    - `Token`: Contém `access_token` JWT e `token_type` (geralmente "bearer").

    **Raises**:
    - `HTTPException` com status 401 se credenciais incorretas.
    - `HTTPException` com status 404 se usuário não existir.
    """
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    token = await authenticate_user(db, user_login)
    return token


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Recupera os detalhes do perfil do usuário autenticado.

    **Parameters**:
    - `token (str)`: Token JWT extraído do cabeçalho `Authorization` (Bearer Token).

    **Returns**:
    - `UserResponse`: Dados do usuário autenticado.

    **Raises**:
    - `HTTPException` com status 401 se o token for inválido, ausente ou expirado.
    """
    current_user = await get_current_user(db, token)
    return current_user
