import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
from app.config import settings
from app.database import SessionLocal
from app.models import User
from app.routes import auth, products, orders, reviews, webhooks, categories, cart
from app.utils.security import hash_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title='Ecommerce API', version='1.0.0')
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(',')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def bootstrap_super_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == settings.super_admin_email).first()
        if not existing:
            user = User(
                email=settings.super_admin_email,
                password_hash=hash_password(settings.super_admin_password),
                first_name=settings.super_admin_first_name,
                last_name=settings.super_admin_last_name,
                is_admin=True,
                is_active=True,
            )
            db.add(user)
            db.commit()
            logger.info('Super admin inicializado: %s', settings.super_admin_email)
    finally:
        db.close()


@app.middleware('http')
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response


app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(webhooks.router)


@app.get('/')
@limiter.limit('30/minute')
def health(_: Request):
    return {'status': 'ok'}
