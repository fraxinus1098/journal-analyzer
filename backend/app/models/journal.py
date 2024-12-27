# File: backend/app/models/journal.py
"""
SQLAlchemy models for journal entries and analysis results.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector
from pydantic import BaseModel, Field
from typing import Optional, List

Base = declarative_base()

class JournalEntry(Base):
    """SQLAlchemy model for journal entries"""
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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