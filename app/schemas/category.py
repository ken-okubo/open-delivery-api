from pydantic import BaseModel, Field, HttpUrl
import uuid
from typing import Optional, List, Literal


class ImageData(BaseModel):
    URL: Optional[HttpUrl]
    CRC_32: Optional[str] = Field(None, alias="CRC-32")


class CategoryBase(BaseModel):
    index: int
    name: str = Field(..., max_length=150)
    description: Optional[str] = None
    image: Optional[ImageData] = None
    externalCode: str
    status: Literal["AVAILABLE", "UNAVAILABLE"] = "AVAILABLE"
    availabilityId: Optional[List[uuid.UUID]] = None
    itemOfferId: Optional[List[uuid.UUID]] = None


class CategoryCreate(CategoryBase):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)

    class Config:
        populate_by_name = True


class CategorySchema(CategoryBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
        populate_by_name = True


class CategoryResponse(CategorySchema):
    pass
