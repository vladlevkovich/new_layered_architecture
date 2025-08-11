from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

# class CartItemOut(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: int
#     quantity: int
#     dish_id: int
#
#
# class CartOut(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: int
#     items: List[CartItemOut]


class CartOut(BaseModel):
    id: int
    user_id: int
    updated_at: datetime


class CartItemCreate(BaseModel):
    dish_id: int
    quantity: int = 1


class CartItemSchema(BaseModel):
    id: int
    name: str
    description: str
    photo: Optional[str]
    price: float
    is_available: bool

    model_config = ConfigDict(from_attributes=True)


class CartItemOutResponseSchema(BaseModel):
    id: int
    quantity: int
    dish: CartItemSchema
    model_config = ConfigDict(from_attributes=True)


class CartItemOutSchema(BaseModel):
    dish: List[CartItemOutResponseSchema]
    total_price: float
    model_config = ConfigDict(from_attributes=True)
