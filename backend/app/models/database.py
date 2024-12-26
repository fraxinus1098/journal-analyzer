from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from .journal import JournalEntry

class VectorEntry(BaseModel):
    """Model for vector storage"""
    id: int
    embedding: List[float]
    entry_id: int
    created_at: datetime
    metadata: dict = {}

class StorageMetrics(BaseModel):
    """Model for storage metrics"""
    total_entries: int
    total_vectors: int
    avg_vector_size: float
    storage_size: str
    index_size: str 