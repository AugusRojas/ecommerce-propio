from datetime import timedelta
from fastapi import HTTPException
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User
from app.schemas.user import UserRegister, UserUpdate
from app.utils.security import create_token, decode_token, hash_password, verify_password


def _to_user_out(user: User) -> dict:
    return {
        'id': str(user.id),
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_admin': user.is_admin,
    }


def _issue_tokens(user_id: str):
    access = create_token(user_id, timedelta(minutes=settings.access_token_expire_minutes), 'access')
    refresh = create_token(user_id, timedelta(days=settings.refresh_token_expire_days), 'refresh')
    return {'access_token': access, 'refresh_token': refresh, 'token_type': 'bearer'}


def register_user(db: Session, payload: UserRegister):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Email en uso')

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'user': _to_user_out(user), **_issue_tokens(str(user.id))}


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    return {'user': _to_user_out(user), **_issue_tokens(str(user.id))}


def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail='Refresh token inválido') from exc

    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='Token incorrecto para refresh')

    user = db.query(User).filter(User.id == payload.get('sub')).first()
    if not user:
        raise HTTPException(status_code=401, detail='Usuario no encontrado')

    return {'access_token': create_token(str(user.id), timedelta(minutes=settings.access_token_expire_minutes), 'access'), 'token_type': 'bearer'}


def update_profile(db: Session, user: User, payload: UserUpdate):
    data = payload.model_dump(exclude_unset=True)
    if 'password' in data:
        user.password_hash = hash_password(data.pop('password'))
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return _to_user_out(user)


def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {'message': 'Si el email existe, recibirás instrucciones de recuperación.'}

    reset_token = create_token(str(user.id), timedelta(minutes=30), 'password_reset')
    # En producción: enviar por email. Por ahora devolvemos token para testing.
    return {
        'message': 'Token de recuperación generado',
        'reset_token': reset_token,
        'expires_in_minutes': 30,
    }


def reset_password(db: Session, token: str, new_password: str):
    try:
        payload = decode_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail='Token de recuperación inválido') from exc

    if payload.get('type') != 'password_reset':
        raise HTTPException(status_code=401, detail='Token no válido para recuperación')

    user = db.query(User).filter(User.id == payload.get('sub')).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')

    user.password_hash = hash_password(new_password)
    db.commit()
    return {'message': 'Contraseña actualizada correctamente'}
