from fastapi import APIRouter

from api.v1.user import router as user_router
from api.v1.invention import router as invention_router
from api.v1.inventor import router as inventor_router
from api.v1.unit import router as unit_router
from api.v1.ticket import router as ticket_router
from api.v1.laboratory import router as laboratory_router
from api.v1.owner import router as owner_router
from api.v1.invention_owner import router as invention_owner_router
from api.v1.inventor_invention import router as inventor_invention_router
from api.v1.admin import router as admin_router


router = APIRouter()

router.include_router(user_router)

router.include_router(admin_router)
router.include_router(invention_router)
router.include_router(inventor_router)
router.include_router(unit_router)
router.include_router(ticket_router)
router.include_router(laboratory_router)
router.include_router(owner_router)
router.include_router(invention_owner_router)
router.include_router(inventor_invention_router)
