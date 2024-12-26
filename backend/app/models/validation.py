from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
import re

class JournalEntryValidation(BaseModel):
    """Validation model for journal entries"""
    date: datetime
    content: str = Field(..., min_length=10, max_length=50000)
    word_count: int = Field(..., gt=0)
    year: int = Field(..., ge=2019, le=2024)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    metadata: dict = Field(default_factory=dict)

    @validator('content')
    def validate_content(cls, v):
        # Check for common PDF artifacts
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', v):
            raise ValueError("Content contains invalid characters")
        
        # Check for reasonable content structure
        if not any(char.isalpha() for char in v):
            raise ValueError("Content must contain at least one letter")
        
        # Check for excessive whitespace
        if len(v.strip()) < len(v) * 0.5:
            raise ValueError("Content contains excessive whitespace")
        
        return v.strip()

    @validator('date')
    def validate_date(cls, v):
        # Ensure date is within valid range
        min_date = datetime(2019, 1, 1)
        max_date = datetime(2024, 12, 31)
        
        if v < min_date or v > max_date:
            raise ValueError(f"Date must be between {min_date.date()} and {max_date.date()}")
        
        return v

    @validator('word_count')
    def validate_word_count(cls, v, values):
        if 'content' in values:
            actual_count = len(values['content'].split())
            if abs(v - actual_count) > 5:  # Allow small discrepancy
                raise ValueError(f"Word count mismatch: got {v}, expected ~{actual_count}")
        return v 