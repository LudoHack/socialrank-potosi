from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

def _build_url(url: str) -> str:
    """Adapta la URL según el driver disponible."""
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        # Heroku/Railway usan postgres://, SQLAlchemy necesita postgresql://
        url = url.replace("postgres://", "postgresql://", 1)
        # Usar psycopg3 (instalado)
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

db_url = _build_url(settings.database_url)

# SQLite no necesita pool_pre_ping ni opciones especiales
connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

engine = create_engine(db_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
