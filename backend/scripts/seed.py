from app.database import Base, SessionLocal, engine
from app.schemas.auth import UserRegister
from app.services.auth_service import create_user, get_user_by_email

SEED_USERS = [
    UserRegister(email="admin@example.com", password="admin1234", first_name="Admin", last_name="Root"),
    UserRegister(email="cliente1@example.com", password="cliente1234", first_name="Juan", last_name="Perez"),
    UserRegister(email="cliente2@example.com", password="cliente1234", first_name="Ana", last_name="Gomez"),
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for payload in SEED_USERS:
            if not get_user_by_email(db, payload.email):
                create_user(db, payload)
        print("Seed completado")
    finally:
        db.close()


if __name__ == "__main__":
    run()
