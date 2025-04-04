import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.utils.serializers import JSONSerializable


menu_category = Table(
    "menu_category",
    Base.metadata,
    Column(
        "menu_id", UUID(as_uuid=True), ForeignKey("menus.id"), primary_key=True
    ),
    Column(
        "category_id",
        UUID(as_uuid=True),
        ForeignKey("categories.id"),
        primary_key=True,
    ),
)


class Menu(Base):
    __tablename__ = "menus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    externalCode = Column(String, nullable=False, unique=True)
    disclaimer = Column(String, nullable=True)
    disclaimerURL = Column(JSONSerializable, nullable=True)

    categories = relationship("Category", secondary=menu_category)
