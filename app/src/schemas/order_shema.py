from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .user_schema import UserResponse


class OrderCreateResponse(BaseModel):
    id: int
    user_id: int
    delivery_time: datetime
    is_ready: bool
    is_notified: bool
    created_at: datetime


class DishSchema(BaseModel):
    id: int
    name: str
    description: str
    photo: Optional[str]
    price: float
    is_available: bool
    model_config = ConfigDict(from_attributes=True)


class OrderItemSchema(BaseModel):
    id: int
    quantity: int
    dish: DishSchema
    model_config = ConfigDict(from_attributes=True)


class OrderSchema(BaseModel):
    id: int
    user_id: int
    delivery_time: datetime
    is_ready: bool
    is_notified: bool
    created_at: datetime
    items: List[OrderItemSchema]
    model_config = ConfigDict(from_attributes=True)


class OrderItemReport(BaseModel):
    id: int
    user: UserResponse
    delivery_time: datetime
    created_at: datetime
    is_ready: bool
    items: List[OrderItemSchema]
