from pydantic import BaseModel, Field, HttpUrl
import uuid
from typing import Optional, List, Literal


class NutritionalInfo(BaseModel):
    description: Optional[str]
    calories: Optional[str]
    allergen: Optional[List[str]] = []
    additives: Optional[List[str]] = []
    suitableDiet: Optional[List[str]] = []
    isAlcoholic: Optional[bool] = False


class ImageData(BaseModel):
    URL: Optional[HttpUrl]
    CRC_32: Optional[str] = Field(None, alias="CRC-32")


class ItemBase(BaseModel):
    name: str
    description: str
    externalCode: str
    status: Optional[Literal["AVAILABLE", "UNAVAILABLE"]] = "AVAILABLE"
    image: Optional[ImageData] = None
    images: Optional[List[ImageData]] = []
    nutritionalInfo: Optional[NutritionalInfo] = None
    serving: Optional[int] = None
    unit: Literal["UN", "KG", "L", "OZ", "LB", "GAL"]
    ean: Optional[str] = None


class ItemCreate(ItemBase):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)


class ItemSchema(ItemBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
        populate_by_name = True
