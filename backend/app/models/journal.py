# File: backend/app/models/journal.py
"""
SQLAlchemy models for journal entries and analysis results.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialogs import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from typing import Optional, List

Base = declarative_base()

class JournalEntry(BaseModel):
    """Model for a journal entry"""
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