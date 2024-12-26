# File: backend/app/models/journal.py
"""
SQLAlchemy models for journal entries and analysis results.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialogs import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    embedding = Column(ARRAY(Float, dimensions=256))  # OpenAI embeddings
    created_at = Column(DateTime, default=datetime.utcnow)
    # TODO: Add additional fields

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    entry_id = Column(Integer, ForeignKey("journal_entries.id"))
    analysis_type = Column(String)  # e.g., "emotional", "topic", "style"
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    # TODO: Add additional fields