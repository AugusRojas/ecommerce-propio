from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings


def _get_database_url() -> str:
    if not settings.database_url:
        raise RuntimeError('DATABASE_URL is required and must point to Supabase Postgres (web).')

    if not settings.database_url.startswith('postgresql+psycopg://'):
        raise RuntimeError('DATABASE_URL must use postgresql+psycopg:// for Python 3.14 compatibility.')

    return settings.database_url


DATABASE_URL = _get_database_url()
engine_kwargs = {'future': True}
if settings.db_use_null_pool:
    engine_kwargs['poolclass'] = NullPool

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
