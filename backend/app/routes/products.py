from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas.product import ProductCreate
from app.services.product_service import list_products
from app.utils.dependencies import get_admin_user

router = APIRouter(prefix='/api/products', tags=['products'])

@router.get('')
def products(q: str | None = None, category_id: str | None = None, skip: int = 0, limit: int = Query(default=20, le=100), db: Session = Depends(get_db)):
    return list_products(db, q, category_id, skip, limit)

@router.get('/{id}')
def detail(id: str, db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.id == id).first()

@router.post('')
def create(payload: ProductCreate, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put('/{id}')
def update(id: str, payload: ProductCreate, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    p = db.query(Product).filter(Product.id == id).first()
    for k, v in payload.model_dump().items():
        setattr(p, k, v)
    db.commit()
    return p

@router.delete('/{id}')
def remove(id: str, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    p = db.query(Product).filter(Product.id == id).first()
    db.delete(p)
    db.commit()
    return {'ok': True}
