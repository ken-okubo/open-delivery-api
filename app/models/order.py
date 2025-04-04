from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from enum import Enum as PyEnum
from app.db.database import Base
from app.utils.serializers import JSONSerializable
from datetime import datetime


class OrderType(str, PyEnum):
    DELIVERY = "DELIVERY"


class OrderStatus(str, PyEnum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    display_id = Column(String, nullable=False)
    type = Column(
        SqlEnum(OrderType), default=OrderType.DELIVERY, nullable=False
    )
    status = Column(
        SqlEnum(OrderStatus), default=OrderStatus.CREATED, nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)

    items = relationship("OrderItem", back_populates="order", lazy="selectin")
    customer = relationship(
        "OrderCustomer", back_populates="order", uselist=False, lazy="selectin")
    delivery = relationship(
        "OrderDelivery", back_populates="order", uselist=False, lazy="selectin")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    item_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")


class OrderCustomer(Base):
    __tablename__ = "order_customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)

    order = relationship("Order", back_populates="customer")


class OrderDelivery(Base):
    __tablename__ = "order_deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    address = Column(JSONSerializable, nullable=False)
    estimated_time = Column(DateTime)
    delivered_time = Column(DateTime)

    order = relationship("Order", back_populates="delivery")
