from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connector import get_db
from repositories.invention_repositories import get_inventions
from schemas.invention import InventionResponse
from schemas.inventor import InventorResponse
from schemas.owner import OwnerResponse
from schemas.unit import UnitResponse

router = APIRouter(tags=["vitrine"])

@router.get("/invencoes")
async def get_invencoes_vitrine_endpoint(
        start: int = 0,
        limit: int = 20,
        db: AsyncSession = Depends(get_db)
):
    invencoes = await get_inventions(db, start, limit)

    response = []
    for inv in invencoes:
        response.append(
            {
                "invention": InventionResponse.model_validate(inv),
                "unit": UnitResponse.model_validate(inv.unit),
                "inventors": [InventorResponse.model_validate(rel.inventor) for rel in inv.inventors],
                "owners": [OwnerResponse.model_validate(rel.owner) for rel in inv.owners],
            }
        )
    return response