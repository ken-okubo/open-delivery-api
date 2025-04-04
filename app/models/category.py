import uuid
from enum import Enum
from sqlalchemy import Column, String, Text, Integer, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.db.database import Base
from app.utils.serializers import JSONSerializable


class Status(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index = Column(Integer, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    # Use JSONSerializable para tratar o objeto com URL
    image = Column(JSONSerializable, nullable=True)
    externalCode = Column(String, nullable=False, unique=True)
    status = Column(SqlEnum(Status), nullable=False, default=Status.AVAILABLE)
    availabilityId = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    itemOfferId = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
