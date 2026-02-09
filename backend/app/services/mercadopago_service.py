import mercadopago
from app.config import settings

sdk = mercadopago.SDK(settings.mercadopago_access_token)

def create_payment_preference(order_id: str, amount: float):
    preference_data = {'items': [{'title': f'Orden {order_id}', 'quantity': 1, 'unit_price': amount}]}
    return sdk.preference().create(preference_data)
