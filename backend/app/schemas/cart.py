from pydantic import BaseModel


class CartItemOut(BaseModel):
    id: str
    product_id: str
    quantity: int

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: str
    user_id: str
    items: list[CartItemOut]

    class Config:
        from_attributes = True
