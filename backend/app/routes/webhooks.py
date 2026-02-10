from fastapi import APIRouter

router = APIRouter(tags=['payments'])

@router.post('/api/checkout/create-preference')
def create_preference(payload: dict):
    return {'status': 'pending', 'payload': payload}

@router.post('/api/webhooks/mercadopago')
def webhook(payload: dict):
    return {'received': True, 'payload': payload}

@router.get('/api/admin/stats')
def stats():
    return {'sales': 0, 'orders': 0, 'users': 0}
