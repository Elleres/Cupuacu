from sqlalchemy.exc import IntegrityError

from const.const import INITIAL_ADMIN_NAME, INITIAL_ADMIN_EMAIL, INITIAL_ADMIN_USERNAME, INITIAL_ADMIN_PASSWORD
from const.enum import UserType
from db.db_connector import get_db
from repositories.user_repositories import create_user
from schemas.user import UserCreate
from services.auth_service import hash_password


async def create_initial_admin_acc():
    async for db in get_db():
        password = await hash_password(INITIAL_ADMIN_PASSWORD)
        admin = UserCreate(
            name=INITIAL_ADMIN_NAME,
            email=INITIAL_ADMIN_EMAIL,
            username=INITIAL_ADMIN_USERNAME,
            password=password,
            type=UserType.admin,
        )
        try:
            await create_user(db, admin)
        except IntegrityError:
            pass