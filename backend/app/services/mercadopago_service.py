"""Mercado Pago integration via REST API (compatible with Python 3.14)."""

import httpx
from app.config import settings


def create_payment_preference(order_id: str, amount: float):
    payload = {
        'items': [
            {
                'title': f'Orden {order_id}',
                'quantity': 1,
                'currency_id': 'ARS',
                'unit_price': float(amount),
            }
        ]
    }
    headers = {
        'Authorization': f'Bearer {settings.mercadopago_access_token}',
        'Content-Type': 'application/json',
    }

    response = httpx.post('https://api.mercadopago.com/checkout/preferences', json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
