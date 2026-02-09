from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str

class ReviewOut(BaseModel):
    id: str
    rating: int
    comment: str
    user_id: str
