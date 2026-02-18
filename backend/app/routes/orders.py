from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order
from app.schemas.order import OrderCreate
from app.services.order_service import create_order, cleanup_expired_pending_orders, update_order_status
from app.utils.dependencies import get_current_user, get_admin_user

router = APIRouter(prefix='/api/orders', tags=['orders'])


@router.post('')
def create(payload: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_order(db, user, payload)


@router.get('')
def list_user_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cleanup_expired_pending_orders(db)
    return db.query(Order).filter(Order.user_id == user.id).all()


@router.get('/{id}')
def detail(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cleanup_expired_pending_orders(db)
    return db.query(Order).filter(Order.id == id, Order.user_id == user.id).first()


@router.get('/{id}/tracking')
def tracking(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Orden no encontrada')
    return {
        'order_id': str(order.id),
        'status': order.status,
        'tracking_code': order.tracking_code,
        'events': order.tracking_events or [],
        'reserved_until': order.reserved_until,
    }


@router.put('/{id}/status')
def update_status(id: str, payload: dict, db: Session = Depends(get_db), _=Depends(get_admin_user)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Orden no encontrada')
    return update_order_status(db, order, payload.get('status', order.status))
