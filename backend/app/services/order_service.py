from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Order, OrderItem, Product, User
from app.schemas.order import OrderCreate
from app.config import settings


def _event(status: str, message: str):
    return {'status': status, 'message': message, 'at': datetime.now(timezone.utc).isoformat()}


def cleanup_expired_pending_orders(db: Session):
    now = datetime.now(timezone.utc)
    expired_orders = db.query(Order).filter(Order.status == 'pending', Order.reserved_until.isnot(None), Order.reserved_until < now).all()
    for order in expired_orders:
        db.delete(order)
    if expired_orders:
        db.commit()


def create_order(db: Session, user: User, payload: OrderCreate):
    cleanup_expired_pending_orders(db)
    total = 0.0
    reserve_until = datetime.now(timezone.utc) + timedelta(hours=settings.order_hold_hours)
    order = Order(
        user_id=user.id,
        shipping_address=payload.shipping_address,
        total=0,
        status='pending',
        reserved_until=reserve_until,
        tracking_code=f'TRK-{str(user.id)[:8]}-{int(datetime.now().timestamp())}',
        tracking_events=[_event('pending', f'Orden creada. Reserva de stock por {settings.order_hold_hours}h.')],
    )
    db.add(order)
    db.flush()

    for item in payload.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            raise HTTPException(status_code=400, detail='Stock insuficiente')
        subtotal = float(product.price) * item.quantity
        total += subtotal
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, price=product.price))

    order.total = total
    db.commit()
    db.refresh(order)
    return order


def mark_order_paid(db: Session, order: Order, mercadopago_id: str = '', mercadopago_status: str = 'approved'):
    if order.status != 'pending':
        return order

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product or product.stock < item.quantity:
            order.status = 'cancelled'
            order.mercadopago_status = 'rejected_stock'
            events = list(order.tracking_events or [])
            events.append(_event('cancelled', 'Pago recibido pero sin stock disponible.'))
            order.tracking_events = events
            db.commit()
            raise HTTPException(status_code=409, detail='Stock no disponible al confirmar pago')

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        product.stock -= item.quantity

    order.status = 'paid'
    order.mercadopago_id = mercadopago_id
    order.mercadopago_status = mercadopago_status
    events = list(order.tracking_events or [])
    events.append(_event('paid', 'Pago confirmado. Stock descontado.'))
    order.tracking_events = events
    db.commit()
    db.refresh(order)
    return order


def update_order_status(db: Session, order: Order, new_status: str):
    order.status = new_status
    events = list(order.tracking_events or [])
    events.append(_event(new_status, f'Estado actualizado a {new_status}.'))
    order.tracking_events = events
    db.commit()
    db.refresh(order)
    return order
