from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Review, Product, Order, OrderItem
from app.schemas.review import ReviewCreate
from app.utils.dependencies import get_current_user

router = APIRouter(tags=['reviews'])

@router.post('/api/products/{id}/reviews')
def create_review(id: str, payload: ReviewCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    purchased = db.query(OrderItem).join(Order, OrderItem.order_id == Order.id).filter(Order.user_id == user.id, OrderItem.product_id == id).first()
    if not purchased:
        raise HTTPException(status_code=403, detail='Debes comprar para opinar')
    review = Review(user_id=user.id, product_id=id, rating=payload.rating, comment=payload.comment)
    db.add(review)
    db.commit()
    avg = db.query(func.avg(Review.rating)).filter(Review.product_id == id).scalar() or 0
    product = db.query(Product).filter(Product.id == id).first()
    if product:
      product.average_rating = float(avg)
      db.commit()
    return review

@router.get('/api/products/{id}/reviews')
def get_reviews(id: str, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.product_id == id).all()

@router.put('/api/reviews/{id}')
def update_review(id: str, payload: ReviewCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == id, Review.user_id == user.id).first()
    review.rating = payload.rating
    review.comment = payload.comment
    db.commit()
    return review

@router.delete('/api/reviews/{id}')
def delete_review(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == id, Review.user_id == user.id).first()
    db.delete(review)
    db.commit()
    return {'ok': True}
