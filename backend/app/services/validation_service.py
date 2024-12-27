from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from ..models.validation import JournalEntryValidation
from ..models.journal import JournalEntry
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class ValidationService:
    def __init__(self):
        self.validation_errors: List[Dict[str, Any]] = []
    
    def validate_entries(self, entries: List[JournalEntry]) -> List[JournalEntry]:
        """Validate a list of journal entries"""
        validated_entries = []
        
        for entry in entries:
            try:
                # Convert to validation model
                validated = JournalEntryValidation(
                    date=entry.date,
                    content=entry.content,
                    word_count=entry.word_count,
                    year=entry.year,
                    month=entry.month,
                    day=entry.day,
                    metadata=entry.metadata
                )
                
                # Additional custom validations
                if self._check_entry_consistency(validated):
                    validated_entries.append(entry)
                else:
                    self._log_validation_error(entry, "Failed consistency check")
                    
            except ValidationError as e:
                self._log_validation_error(entry, str(e))
                continue
            
        return validated_entries
    
    def _check_entry_consistency(self, entry: JournalEntryValidation) -> bool:
        """Additional consistency checks"""
        try:
            # Check date components match
            if (entry.year != entry.date.year or 
                entry.month != entry.date.month or 
                entry.day != entry.date.day):
                self._log_validation_error(entry, "Date components mismatch")
                return False
            
            # Check for future dates
            if entry.date > datetime.now():
                self._log_validation_error(entry, "Future date detected")
                return False
            
            # Check for reasonable content length per word
            avg_word_length = len(entry.content) / entry.word_count if entry.word_count > 0 else 0
            if avg_word_length > 15:  # Suspicious if average word is too long
                self._log_validation_error(entry, f"Suspicious average word length: {avg_word_length}")
                return False
            
            return True
            
        except Exception as e:
            self._log_validation_error(entry, f"Consistency check error: {str(e)}")
            return False
    
    def _log_validation_error(self, entry: Any, error: str):
        """Log validation errors for later analysis"""
        error_entry = {
            "date": getattr(entry, "date", None),
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.validation_errors.append(error_entry)
        logger.warning(f"Validation error: {error_entry}")
    
    def get_validation_errors(self) -> List[Dict[str, Any]]:
        """Return all validation errors"""
        return self.validation_errors 