from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
from app.config import get_settings
from app.models.database import Base

settings = get_settings()

# Create engine with appropriate settings for SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    poolclass=StaticPool,  # Use StaticPool for SQLite
    echo=settings.debug  # Log SQL queries in debug mode
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database by creating all tables."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def drop_db() -> None:
    """Drop all tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
    print("⚠️  Database tables dropped!")