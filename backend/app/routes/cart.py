from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.cart import Cart
from app.schemas.cart import CartOut
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("", response_model=CartOut)
def get_my_cart(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    cart = (
        db.query(Cart)
        .options(joinedload(Cart.items))
        .filter(Cart.user_id == current_user.id)
        .first()
    )
    return cart
