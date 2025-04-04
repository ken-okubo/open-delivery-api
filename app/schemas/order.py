from pydantic import BaseModel
import uuid
from typing import Optional, List, Literal
from datetime import datetime


class AddressSchema(BaseModel):
    street: str
    number: str
    city: str
    state: str
    postal_code: str
    complement: Optional[str] = None


class OrderItemSchema(BaseModel):
    id: uuid.UUID
    item_id: uuid.UUID
    name: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class OrderCustomerSchema(BaseModel):
    id: uuid.UUID
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class OrderDeliverySchema(BaseModel):
    id: uuid.UUID
    address: AddressSchema
    estimated_time: Optional[datetime] = None
    delivered_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: uuid.UUID
    display_id: str
    type: Literal["DELIVERY"]
    status: Literal[
        "CREATED", "CONFIRMED", "DISPATCHED", "DELIVERED", "CANCELLED"
    ]
    created_at: datetime
    total_amount: float
    items: List[OrderItemSchema] = []
    customer: Optional[OrderCustomerSchema] = None
    delivery: Optional[OrderDeliverySchema] = None

    class Config:
        from_attributes = True


class OrderUpdateSchema(BaseModel):
    status: Literal["CONFIRMED", "DISPATCHED", "DELIVERED", "CANCELLED"]
    reason: Optional[str] = None


class OrderItemCreateSchema(BaseModel):
    item_id: uuid.UUID
    name: str
    quantity: int
    unit_price: float


class OrderCustomerCreateSchema(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class OrderDeliveryCreateSchema(BaseModel):
    address: AddressSchema
    estimated_time: Optional[datetime] = None


class OrderCreateSchema(BaseModel):
    display_id: str
    type: Literal["DELIVERY"] = "DELIVERY"
    total_amount: float
    items: List[OrderItemCreateSchema]
    customer: OrderCustomerCreateSchema
    delivery: OrderDeliveryCreateSchema
