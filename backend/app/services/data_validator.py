"""
Service for validating journal entries.
"""
from datetime import datetime
from typing import List, Optional
import logging
from ..models.journal import JournalEntrySchema

logger = logging.getLogger(__name__)

class DataValidator:
    def __init__(self):
        self.min_content_length = 10  # Minimum characters for valid entry
        self.max_content_length = 50000  # Maximum characters for valid entry
        
    def validate_entries(self, entries: List[JournalEntrySchema]) -> List[JournalEntrySchema]:
        """
        Validate a list of journal entries.
        Returns only valid entries and logs validation failures.
        """
        valid_entries = []
        seen_dates = set()
        
        # Sort entries by date for chronological validation
        sorted_entries = sorted(entries, key=lambda x: x.date)
        
        for entry in sorted_entries:
            validation_result = self._validate_entry(entry, seen_dates)
            if validation_result.is_valid:
                valid_entries.append(entry)
                seen_dates.add(entry.date.date())
            else:
                logger.warning(f"Entry validation failed: {validation_result.error}")
        
        return valid_entries
    
    def _validate_entry(self, entry: JournalEntrySchema, seen_dates: set) -> 'ValidationResult':
        """
        Validate a single journal entry.
        """
        # Check for future dates
        if entry.date > datetime.now():
            return ValidationResult(False, "Entry date is in the future")
        
        # Check for duplicate dates
        if entry.date.date() in seen_dates:
            return ValidationResult(False, f"Duplicate entry for date {entry.date.date()}")
        
        # Validate content length
        if len(entry.content) < self.min_content_length:
            return ValidationResult(False, "Entry content too short")
        if len(entry.content) > self.max_content_length:
            return ValidationResult(False, "Entry content too long")
        
        # Validate word count
        if entry.word_count == 0:
            return ValidationResult(False, "Entry has no words")
        
        # Validate date components
        if not self._validate_date_components(entry):
            return ValidationResult(False, "Invalid date components")
        
        return ValidationResult(True)
    
    def _validate_date_components(self, entry: JournalEntrySchema) -> bool:
        """
        Validate that date components (year, month, day) match the entry date.
        """
        return (
            entry.year == entry.date.year and
            entry.month == entry.date.month and
            entry.day == entry.date.day
        )

class ValidationResult:
    def __init__(self, is_valid: bool, error: str = ""):
        self.is_valid = is_valid
        self.error = error 