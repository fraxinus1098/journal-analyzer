# File: backend/app/models/journal.py
"""
SQLAlchemy models for journal entries and analysis results.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.sql import func

Base = declarative_base()

class JournalEntry(Base):
    """SQLAlchemy model for journal entries"""
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    
    # Core Entry Data
    entry_date = Column(DateTime, nullable=False, index=True)
    content = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False, default=0)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False, index=True)
    day = Column(Integer, nullable=False)
    
    # Analysis Data (nullable for now)
    sentiment_score = Column(Float, nullable=True)
    complexity_score = Column(Float, nullable=True)
    topics = Column(JSON, nullable=True)
    mentioned_people = Column(JSON, nullable=True)
    mentioned_locations = Column(JSON, nullable=True)
    
    # Vector Embedding (1536 dimensions for OpenAI embeddings)
    embedding = Column(Vector(1536), nullable=True)
    
    # Metadata
    source_file = Column(String, nullable=False)
    entry_number = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class JournalEntrySchema(BaseModel):
    """Pydantic model for API interactions"""
    date: datetime
    content: str
    word_count: int = Field(default=0)
    year: int = Field(...)
    month: int = Field(...)
    day: int = Field(...)
    metadata: dict = Field(default_factory=dict)
    
    class Config:
        from_attributes = True

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    analysis_type = Column(String)  # e.g., "emotional", "topic", "style"
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    # TODO: Add additional fields