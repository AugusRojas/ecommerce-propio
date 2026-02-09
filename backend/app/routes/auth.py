from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user
from app.utils.dependencies import get_current_user

router = APIRouter(prefix='/api/auth', tags=['auth'])

@router.post('/register')
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)

@router.post('/login')
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, payload.email, payload.password)

@router.post('/refresh')
def refresh():
    return {'message': 'Use refresh token strategy in production'}

@router.get('/me')
def me(user=Depends(get_current_user)):
    return user

@router.put('/me')
def update_me(data: dict, user=Depends(get_current_user)):
    return {'message': 'updated', 'data': data, 'user_id': str(user.id)}
