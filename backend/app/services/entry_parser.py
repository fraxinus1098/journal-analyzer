"""
Service for parsing and segmenting journal entries.
"""
import re
from datetime import datetime
from typing import List, Dict, Any
import logging
from ..models.journal import JournalEntrySchema

logger = logging.getLogger(__name__)

class EntryParser:
    # Common date patterns in journal entries
    DATE_PATTERNS = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',  # MM/DD/YYYY or MM-DD-YYYY
        r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',     # YYYY/MM/DD or YYYY-MM-DD
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
    ]
    
    def __init__(self):
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.DATE_PATTERNS]
    
    def parse_entries(self, content: List[Dict[str, Any]]) -> List[JournalEntrySchema]:
        """
        Parse PDF content into individual journal entries.
        """
        entries = []
        current_entry = ""
        current_date = None
        
        for page in content:
            text = page['text']
            
            # Split text into potential entries
            segments = self._split_by_dates(text)
            
            for date_str, entry_text in segments:
                try:
                    entry_date = self._parse_date(date_str)
                    if entry_date and entry_text.strip():
                        entry = self._create_entry(entry_date, entry_text.strip())
                        entries.append(entry)
                except Exception as e:
                    logger.warning(f"Failed to parse entry with date {date_str}: {str(e)}")
                    continue
        
        return sorted(entries, key=lambda x: x.date)
    
    def _split_by_dates(self, text: str) -> List[tuple[str, str]]:
        """
        Split text into segments based on date patterns.
        Returns list of (date_string, content) tuples.
        """
        segments = []
        last_end = 0
        current_date = None
        
        # Combine all patterns into one search
        for pattern in self.compiled_patterns:
            for match in pattern.finditer(text):
                date_str = match.group(0)
                start_pos = match.start()
                
                # If we have a previous date, save the content
                if current_date:
                    content = text[last_end:start_pos].strip()
                    segments.append((current_date, content))
                
                current_date = date_str
                last_end = match.end()
        
        # Add the final segment
        if current_date:
            segments.append((current_date, text[last_end:].strip()))
            
        return segments
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse a date string into a datetime object.
        Handles multiple date formats.
        """
        formats = [
            "%m/%d/%Y", "%Y/%m/%d",
            "%m-%d-%Y", "%Y-%m-%d",
            "%B %d, %Y", "%B %d %Y"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse date: {date_str}")
    
    def _create_entry(self, date: datetime, content: str) -> JournalEntrySchema:
        """
        Create a JournalEntrySchema instance from parsed data.
        """
        return JournalEntrySchema(
            date=date,
            content=content,
            word_count=len(content.split()),
            year=date.year,
            month=date.month,
            day=date.day,
            metadata={
                "source": "pdf_import",
                "processed_at": datetime.utcnow().isoformat()
            }
        ) 