from pydantic import BaseModel, Field
import uuid
from typing import Optional, List, Literal


class ItemPrice(BaseModel):
    value: float
    originalValue: Optional[float] = None


class ItemOfferBase(BaseModel):
    itemId: uuid.UUID
    index: int
    status: Literal["AVAILABLE", "UNAVAILABLE"] = "AVAILABLE"
    price: ItemPrice
    availabilityId: Optional[List[uuid.UUID]] = None
    optionGroupsId: Optional[List[uuid.UUID]] = None


class ItemOfferCreate(ItemOfferBase):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)


class ItemOfferResponse(ItemOfferCreate):
    class Config:
        from_attributes = True


class ItemOfferSchema(ItemOfferCreate):
    class Config:
        from_attributes = True
