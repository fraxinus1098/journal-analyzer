from datetime import datetime
import re
from typing import List, Dict, Any, Optional
from ..models.journal import JournalEntry
import logging

logger = logging.getLogger(__name__)

class EntryParser:
    def __init__(self):
        self.date_pattern = r"(\d{2}/\d{2}/\d{4})(.*?)(?=\d{2}/\d{2}/\d{4}|$)"
        self.date_format = "%m/%d/%Y"
    
    def parse_entries(self, text: str) -> List[JournalEntry]:
        """Parse journal entries from text content"""
        entries = []
        matches = re.finditer(self.date_pattern, text, re.DOTALL)
        
        current_year = None
        for match in matches:
            try:
                date_str, content = match.groups()
                entry = self._create_entry(date_str.strip(), content.strip())
                
                if entry:
                    # Validate year continuity
                    if current_year and entry.year < current_year:
                        logger.warning(f"Year discontinuity detected: {entry.year} after {current_year}")
                    current_year = entry.year
                    entries.append(entry)
                    
            except Exception as e:
                logger.error(f"Error parsing entry: {str(e)}", exc_info=True)
                continue
        
        return self._validate_and_sort_entries(entries)
    
    def _create_entry(self, date_str: str, content: str) -> Optional[JournalEntry]:
        """Create a journal entry from parsed components"""
        try:
            # Parse date
            date = datetime.strptime(date_str, self.date_format)
            
            # Validate date range (2019-2024)
            if not (2019 <= date.year <= 2024):
                logger.warning(f"Entry date {date_str} outside valid range")
                return None
            
            # Clean and validate content
            if not self._validate_content(content):
                return None
            
            # Create entry
            return JournalEntry(
                date=date,
                content=content,
                word_count=len(content.split()),
                year=date.year,
                month=date.month,
                day=date.day,
                metadata={
                    "original_date_str": date_str,
                    "parsed_timestamp": datetime.now().isoformat()
                }
            )
            
        except ValueError as e:
            logger.error(f"Invalid date format: {date_str}", exc_info=True)
            return None
    
    def _validate_content(self, content: str) -> bool:
        """Validate entry content"""
        # Remove whitespace
        content = content.strip()
        
        # Check minimum length (10 characters)
        if len(content) < 10:
            return False
        
        # Check for obvious errors (e.g., all whitespace)
        if not content.strip():
            return False
        
        # Check for reasonable length (max 50K characters)
        if len(content) > 50000:
            logger.warning(f"Entry content exceeds 50K characters: {len(content)}")
        
        return True
    
    def _validate_and_sort_entries(self, entries: List[JournalEntry]) -> List[JournalEntry]:
        """Validate and sort the complete list of entries"""
        # Sort entries by date
        entries.sort(key=lambda x: x.date)
        
        # Check for duplicate dates
        dates_seen = set()
        unique_entries = []
        
        for entry in entries:
            entry_date = entry.date.date()
            if entry_date in dates_seen:
                logger.warning(f"Duplicate entry found for date: {entry_date}")
                continue
            
            dates_seen.add(entry_date)
            unique_entries.append(entry)
        
        return unique_entries 