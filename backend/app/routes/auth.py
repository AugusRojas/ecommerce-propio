from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserLogin,
    UserOut,
    UserRegister,
)
from app.services.auth_service import create_user, get_user_by_email
from app.utils.dependencies import get_current_user
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return create_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=user,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        decoded = decode_token(payload.refresh_token)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Refresh token inválido") from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token incorrecto")

    user = db.get(User, decoded.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        user=user,
    )


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        return {"message": "Si el correo existe, enviamos instrucciones."}

    reset_token = create_reset_token(user.id)
    return {
        "message": "Token de recuperación generado. En producción envíalo por email.",
        "reset_token": reset_token,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        decoded = decode_token(payload.token)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Token inválido") from exc

    if decoded.get("type") != "reset":
        raise HTTPException(status_code=401, detail="Token incorrecto")

    user = db.get(User, decoded.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.password_hash = hash_password(payload.new_password)
    db.add(user)
    db.commit()
    return {"message": "Contraseña actualizada correctamente"}
