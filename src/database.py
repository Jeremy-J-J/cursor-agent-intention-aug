"""
Database configuration and session management
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

# Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/vw_scenarios"
)

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)