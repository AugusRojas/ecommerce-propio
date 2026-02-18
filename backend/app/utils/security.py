from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from jwt import InvalidTokenError
from app.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))


def create_token(subject: str, expires_delta: timedelta, token_type: str, extra: dict | None = None) -> str:
    payload = {
        'sub': subject,
        'exp': datetime.now(timezone.utc) + expires_delta,
        'type': token_type,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except InvalidTokenError as exc:
        raise InvalidTokenError('Token inválido o expirado') from exc
