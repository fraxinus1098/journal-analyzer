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
        # Drop existing tables
        Base.metadata.drop_all(bind=engine)
        
        # Create pgvector extension
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
        
        # Create tables with new schema
        Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add this function to test database connection
def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Add this to your startup
if __name__ == "__main__":
    test_db_connection()