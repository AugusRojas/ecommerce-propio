from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.schemas.user import UserRegister
from app.utils.security import hash_password, verify_password, create_token
from app.config import settings

def register_user(db: Session, payload: UserRegister):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Email en uso')
    user = User(email=payload.email, password_hash=hash_password(payload.password), first_name=payload.first_name, last_name=payload.last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    access = create_token(str(user.id), timedelta(minutes=settings.access_token_expire_minutes), 'access')
    refresh = create_token(str(user.id), timedelta(days=settings.refresh_token_expire_days), 'refresh')
    return {'access_token': access, 'refresh_token': refresh, 'token_type': 'bearer'}
