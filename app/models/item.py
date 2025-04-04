from sqlalchemy import Column, String, Integer, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from app.db.database import Base
from app.utils.serializers import JSONSerializable


class ItemStatus(str, PyEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class UnitType(str, PyEnum):
    UN = "UN"
    KG = "KG"
    L = "L"
    OZ = "OZ"
    LB = "LB"
    GAL = "GAL"


class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String, nullable=False)
    externalCode = Column(String, nullable=False, unique=True)
    status = Column(
        SqlEnum(ItemStatus), default=ItemStatus.AVAILABLE, nullable=False
    )
    image = Column(JSONSerializable, nullable=True)
    images = Column(JSONSerializable, nullable=True)
    nutritionalInfo = Column(JSONSerializable, nullable=True)
    serving = Column(Integer, nullable=True)
    unit = Column(SqlEnum(UnitType), nullable=False)
    ean = Column(String, nullable=True)
    item_offers = relationship("ItemOffer", back_populates="item")
