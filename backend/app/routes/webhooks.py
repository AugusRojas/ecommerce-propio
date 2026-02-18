from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_service import mark_order_paid

router = APIRouter(tags=['payments'])


@router.post('/api/checkout/create-preference')
def create_preference(payload: dict):
    # frontend should send order_id generated in /api/orders
    return {'status': 'pending', 'preference_for_order': payload.get('order_id')}


@router.post('/api/webhooks/mercadopago')
def webhook(payload: dict, db: Session = Depends(get_db)):
    # Expected payload example:
    # {"order_id":"...", "payment_id":"...", "status":"approved"}
    order_id = payload.get('order_id')
    if not order_id:
        raise HTTPException(status_code=400, detail='order_id requerido')

    status = payload.get('status', '').lower()
    if status == 'approved':
        updated = mark_order_paid(db, order_id, payload.get('payment_id', ''), status)
        return {'received': True, 'order_id': str(updated.id), 'status': updated.status}

    return {'received': True, 'order_id': str(order_id), 'status': 'pending'}


@router.get('/api/admin/stats')
def stats():
    return {'sales': 0, 'orders': 0, 'users': 0}
