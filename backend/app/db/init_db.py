# File: backend/app/db/init_db.py
"""
Database initialization and connection management.
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
from ..models.journal import Base

# Create synchronous engine instead of async
engine = create_engine(settings.DATABASE_URL, echo=True)

# Create synchronous session factory
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Initialize database with required tables."""
    with engine.begin() as conn:
        # Create pgvector extension
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        # Create tables
        Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()