from fastapi import APIRouter

from api.v1.user import router as user_router
from api.v1.invention import router as invention_router


router = APIRouter()

router.include_router(user_router)
router.include_router(invention_router)
