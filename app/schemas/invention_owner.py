from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field



class InventionOwnerCreate(BaseModel):
    id_owner: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    id_invention: UUID = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")


class InventionOwnerResponse(InventionOwnerCreate):
    model_config = ConfigDict(from_attributes=True)
