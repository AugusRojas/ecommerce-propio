from pydantic import BaseModel

class OrderItemIn(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: list[OrderItemIn]
    shipping_address: dict

class OrderOut(BaseModel):
    id: str
    status: str
    total: float
