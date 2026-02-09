from sqlalchemy.orm import Session
from app.models import Product

def list_products(db: Session, q: str | None = None, category_id: str | None = None, skip: int = 0, limit: int = 20):
    query = db.query(Product)
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()
