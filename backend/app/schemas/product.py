from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: str
    images: list[str] = []

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: str
    average_rating: float
