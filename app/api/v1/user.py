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

    **Parâmetros:**
    - `user`: Objeto `UserCreate` contendo os dados do novo usuário (nome, email, username, password e type).

    **Retorna:**
    - `UserResponse`: Objeto contendo os dados do usuário criado, excluindo a senha.

    **Levanta:**
    - `HTTPException` com status 400 se os dados violarem alguma restrição do banco de dados.
    - `HTTPException` com status 500 para erros não documentados.
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
        db: AsyncSession = Depends(get_db)
):
    """
    Processa a requisição para autenticar um usuário e gerar um token de acesso.

    **Parâmetros:**
    - `form_data`: Objeto `OAuth2PasswordRequestForm` contendo o nome de usuário e a senha.
      Estes são esperados como dados de formulário (`application/x-www-form-urlencoded`).

    **Retorna:**
    - `Token`: Objeto contendo o `access_token` JWT e o `token_type` (geralmente "bearer").

    **Levanta:**
    - `HTTPException` com status 401 se as credenciais (username/password) estiverem incorretas.
    - `HTTPException` com status 404 se o username não estiver registrado no banco de dados.
    """
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    token = await authenticate_user(db, user_login)
    return token

@router.get("/me", response_model=UserResponse)
async def read_users_me(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
):
    """
    Recupera os detalhes do perfil do usuário atualmente autenticado.

    **Parâmetros:**
    - `token`: Token de acesso JWT fornecido no cabeçalho `Authorization` (Bearer Token).
      Este parâmetro é injetado automaticamente pelo `oauth2_scheme` e não precisa ser passado explicitamente pelo cliente (SE ESTIVER USANDO O SWAGGER).

    **Retorna:**
    - `UserResponse`: Um objeto contendo os detalhes do usuário autenticado.

    **Levanta:**
    - `HTTPException` com status 401 (Não Autorizado) se o token for inválido, ausente ou expirado.
    """
    current_user = await get_current_user(db, token)

    return current_user
