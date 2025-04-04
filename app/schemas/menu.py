from pydantic import BaseModel, Field, HttpUrl
from app.schemas.category import CategorySchema
import uuid
from typing import Optional, List


class MenuBase(BaseModel):
    name: str = Field(..., max_length=500)
    description: Optional[str] = None
    externalCode: str
    disclaimer: Optional[str] = None
    disclaimerURL: Optional[HttpUrl] = None


class MenuCreate(MenuBase):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    categoryId: List[uuid.UUID] = Field(default=[], alias="category_ids")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class MenuSchema(MenuBase):
    id: uuid.UUID
    categoryId: List[uuid.UUID] = []
    categories: List[CategorySchema] = []

    class Config:
        from_attributes = True
        populate_by_name = True

    @classmethod
    def model_validate(cls, obj):
        menu_dict = {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "externalCode": obj.externalCode,
            "disclaimer": obj.disclaimer,
            "disclaimerURL": obj.disclaimerURL,
            "categoryId": [cat.id for cat in obj.categories],
            "categories": obj.categories,
        }
        return cls.model_construct(**menu_dict)


class MenuResponse(MenuSchema):
    pass
