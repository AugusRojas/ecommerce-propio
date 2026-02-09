from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product, User
from app.schemas.order import OrderCreate

def create_order(db: Session, user: User, payload: OrderCreate):
    total = 0
    order = Order(user_id=user.id, shipping_address=payload.shipping_address, total=0)
    db.add(order)
    db.flush()
    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail='Stock insuficiente')
        product.stock -= item.quantity
        subtotal = float(product.price) * item.quantity
        total += subtotal
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=product.price))
    order.total = total
    db.commit()
    db.refresh(order)
    return order
