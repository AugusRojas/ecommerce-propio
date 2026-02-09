from fastapi import APIRouter

router = APIRouter(prefix='/api/cart', tags=['cart'])

@router.get('')
def get_cart():
    return {'items': []}

@router.post('/items')
def add_item(payload: dict):
    return payload

@router.put('/items/{id}')
def update_item(id: str, payload: dict):
    return {'id': id, **payload}

@router.delete('/items/{id}')
def delete_item(id: str):
    return {'deleted': id}
