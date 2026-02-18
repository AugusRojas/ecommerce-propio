from collections import defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Order, OrderItem, Product, User
from app.schemas.order import OrderCreate


def _event(status: str, message: str):
    return {'status': status, 'message': message, 'at': datetime.now(timezone.utc).isoformat()}


def _aggregate_items(items):
    quantities = defaultdict(int)
    for item in items:
        if item.quantity <= 0:
            raise HTTPException(status_code=422, detail='La cantidad debe ser mayor a 0')
        quantities[str(item.product_id)] += item.quantity
    return quantities


def cleanup_expired_pending_orders(db: Session):
    now = datetime.now(timezone.utc)
    with db.begin():
        expired_orders = (
            db.query(Order)
            .filter(Order.status == 'pending', Order.reserved_until.isnot(None), Order.reserved_until < now)
            .all()
        )
        for order in expired_orders:
            db.delete(order)


def create_order(db: Session, user: User, payload: OrderCreate):
    cleanup_expired_pending_orders(db)

    quantities = _aggregate_items(payload.items)
    reserve_until = datetime.now(timezone.utc) + timedelta(hours=settings.order_hold_hours)

    with db.begin():
        product_ids = list(quantities.keys())
        products = (
            db.query(Product)
            .filter(Product.id.in_(product_ids))
            .all()
        )
        products_map = {str(product.id): product for product in products}

        missing = [pid for pid in product_ids if pid not in products_map]
        if missing:
            raise HTTPException(status_code=404, detail=f'Productos inexistentes: {missing}')

        for pid, qty in quantities.items():
            product = products_map[pid]
            if product.stock < qty:
                raise HTTPException(status_code=409, detail=f'Stock insuficiente para {product.name}')

        order = Order(
            user_id=user.id,
            shipping_address=payload.shipping_address,
            total=0,
            status='pending',
            reserved_until=reserve_until,
            tracking_code=f'TRK-{str(user.id)[:8]}-{int(datetime.now().timestamp())}',
            tracking_events=[_event('pending', f'Orden creada. Reserva por {settings.order_hold_hours}h.')],
        )
        db.add(order)
        db.flush()

        total = Decimal('0')
        for pid, qty in quantities.items():
            product = products_map[pid]
            frozen_price = Decimal(str(product.price))
            subtotal = frozen_price * qty
            total += subtotal
            db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    price=frozen_price,
                )
            )

        order.total = total

    db.refresh(order)
    return order


def mark_order_paid(db: Session, order_id: str, mercadopago_id: str = '', mercadopago_status: str = 'approved'):
    insufficient_stock = False
    insufficient_product = ''

    with db.begin():
        order = db.query(Order).filter(Order.id == order_id).with_for_update().first()
        if not order:
            raise HTTPException(status_code=404, detail='Orden no encontrada')

        if order.status != 'pending':
            return order

        products_by_id = {}
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
            if not product:
                insufficient_stock = True
                insufficient_product = str(item.product_id)
                break
            products_by_id[str(item.product_id)] = product
            if product.stock < item.quantity:
                insufficient_stock = True
                insufficient_product = product.name
                break

        if insufficient_stock:
            order.status = 'cancelled'
            order.mercadopago_status = 'rejected_stock'
            events = list(order.tracking_events or [])
            events.append(_event('cancelled', f'Pago rechazado por stock insuficiente: {insufficient_product}'))
            order.tracking_events = events
        else:
            for item in order.items:
                product = products_by_id[str(item.product_id)]
                product.stock -= item.quantity

            order.status = 'paid'
            order.mercadopago_id = mercadopago_id
            order.mercadopago_status = mercadopago_status
            events = list(order.tracking_events or [])
            events.append(_event('paid', 'Pago confirmado. Stock descontado.'))
            order.tracking_events = events

    if insufficient_stock:
        raise HTTPException(status_code=409, detail='Stock no disponible al confirmar pago')

    db.refresh(order)
    return order


def update_order_status(db: Session, order: Order, new_status: str):
    with db.begin():
        order.status = new_status
        events = list(order.tracking_events or [])
        events.append(_event(new_status, f'Estado actualizado a {new_status}.'))
        order.tracking_events = events
    db.refresh(order)
    return order
