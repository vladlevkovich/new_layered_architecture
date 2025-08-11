from datetime import datetime
from typing import List

from pydantic import BaseModel

from .user_schema import UserResponse


class DishSchema(BaseModel):
    dish_name: str
    price: float


class OrderItemReport(BaseModel):
    # dish: str
    dish_name: str
    quantity: int
    price: float


class OrderReport(BaseModel):
    id: int
    user: UserResponse
    delivery_time: datetime
    created_at: datetime
    is_ready: bool
    items: List[OrderItemReport]


class ReportResponse(BaseModel):
    detail: str
