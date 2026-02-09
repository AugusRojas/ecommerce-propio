from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(subject: str, expires_delta: timedelta, token_type: str) -> str:
    payload = {'sub': subject, 'exp': datetime.now(timezone.utc) + expires_delta, 'type': token_type}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
