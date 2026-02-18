from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.user import User
from app.schemas.auth import UserRegister
from app.utils.security import hash_password


def create_user(db: Session, payload: UserRegister) -> User:
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db.add(user)
    db.flush()

    cart = Cart(user_id=user.id)
    db.add(cart)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()
