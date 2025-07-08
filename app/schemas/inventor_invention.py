from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field



class InventorInventionCreate(BaseModel):
    id_inventor: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    id_invention: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")


class InventorInventionResponse(InventorInventionCreate):
    model_config = ConfigDict(from_attributes=True)
