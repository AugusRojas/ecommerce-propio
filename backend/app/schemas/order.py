from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)
    shipping_address: dict


class OrderOut(BaseModel):
    id: str
    status: str
    total: float
