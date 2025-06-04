from fastapi import APIRouter

from api.v1.user import router as user_router


router = APIRouter()

router.include_router(user_router)
