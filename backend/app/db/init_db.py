# File: backend/app/db/init_db.py
"""
Database initialization and connection management.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.journal import Base

# Create async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Initialize database with required tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)