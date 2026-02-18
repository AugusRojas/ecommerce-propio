from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import (
    ForgotPasswordIn,
    ResetPasswordIn,
    UserLogin,
    UserRegister,
    UserUpdate,
)
from app.services.auth_service import (
    forgot_password,
    login_user,
    refresh_access_token,
    register_user,
    reset_password,
    update_profile,
)
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/api/auth', tags=['auth'])


@router.post('/register')
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post('/login')
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, payload.email, payload.password)


@router.post('/refresh')
def refresh(payload: dict, db: Session = Depends(get_db)):
    return refresh_access_token(db, payload.get('refresh_token', ''))


@router.get('/me')
def me(user=Depends(get_current_user)):
    return {
        'id': str(user.id),
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_admin': user.is_admin,
    }


@router.put('/me')
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_profile(db, user, payload)


@router.post('/forgot-password')
def forgot(payload: ForgotPasswordIn, db: Session = Depends(get_db)):
    return forgot_password(db, payload.email)


@router.post('/reset-password')
def reset(payload: ResetPasswordIn, db: Session = Depends(get_db)):
    return reset_password(db, payload.token, payload.new_password)
