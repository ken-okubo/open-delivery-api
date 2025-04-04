from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from app.db.database import Base
from app.utils.serializers import JSONSerializable


class OfferStatus(str, PyEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class ItemOffer(Base):
    __tablename__ = "item_offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itemId = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)
    index = Column(Integer, nullable=False)
    status = Column(
        Enum(OfferStatus), default=OfferStatus.AVAILABLE, nullable=False
    )
    price = Column(JSONSerializable, nullable=False)
    availabilityId = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    optionGroupsId = Column(ARRAY(UUID(as_uuid=True)), nullable=True)

    item = relationship("Item", back_populates="item_offers")
