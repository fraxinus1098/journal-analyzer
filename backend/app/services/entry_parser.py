"""
Service for parsing and segmenting journal entries.
"""
import re
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class EntryParser:
    DAY_MAPPING = {
        'Sunday': 1,
        'Monday': 2,
        'Tuesday': 3,
        'Wednesday': 4,
        'Thursday': 5,
        'Friday': 6,
        'Saturday': 7
    }

    def __init__(self):
        # Pattern specifically matches your date format with day of week
        self.entry_pattern = r'(\d{1,2}/\d{1,2}/\d{4})\s*[–-]\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)'
        
        # Pattern to identify month headers
        self.month_header = r'^(January|February|March|April|May|June|July|August|September|October|November|December)$'
    
    def parse_date(self, date_str: str) -> datetime.date:
        """
        Parse date string with flexible format handling.
        Accepts M/D/YYYY, MM/DD/YYYY, and variations.
        """
        try:
            # Split the date string into components
            month, day, year = map(int, date_str.split('/'))
            # Create date object directly with integers
            return datetime(year, month, day).date()
        except ValueError as e:
            logger.error(f"Failed to parse date '{date_str}': {str(e)}")
            raise
    
    def parse_entries(self, content: str, source_file: str) -> List[dict]:
        """Parse content into separate journal entries."""
        try:
            if not isinstance(content, str):
                raise ValueError(f"Expected string content, got {type(content)}")
            
            # First, remove month headers
            content = re.sub(self.month_header, '', content, flags=re.MULTILINE)
            
            # Remove any resulting empty lines
            content = re.sub(r'\n\s*\n', '\n', content)
            
            # Split content by entry pattern
            entries_split = re.split(self.entry_pattern, content)
            
            # Remove any empty strings at the start
            if entries_split[0].strip() == '':
                entries_split = entries_split[1:]
            
            entries = []
            
            # Process entries in groups of 3 (date, day, content)
            for i in range(0, len(entries_split), 3):
                if i + 2 >= len(entries_split):
                    break
                    
                date_str = entries_split[i]
                day_str = entries_split[i + 1]
                content_text = entries_split[i + 2].strip()
                
                try:
                    # Parse date using flexible parser
                    date = self.parse_date(date_str)
                    
                    # Get day of week number
                    day_of_week = self.DAY_MAPPING[day_str]
                    
                    # Create entry
                    entry = {
                        'date': date,
                        'content': content_text,
                        'day_of_week': day_of_week,
                        'word_count': len(content_text.split()),
                        'year': date.year,
                        'month': date.month,
                        'day': date.day,
                        'source_file': source_file,
                        'sentiment_score': None,
                        'complexity_score': None,
                        'topics': None,
                        'mentioned_people': None,
                        'mentioned_locations': None,
                        'embedding': None
                    }
                    
                    entries.append(entry)
                    logger.debug(f"Parsed entry for {date}: day={day_str}, content_preview={content_text[:50]}")
                    
                except ValueError as e:
                    logger.warning(f"Skipping entry with invalid date {date_str}: {str(e)}")
                    continue
            
            if not entries:
                raise ValueError("No valid entries were parsed")
            
            logger.info(f"Successfully parsed {len(entries)} entries from {source_file}")
            return entries
            
        except Exception as e:
            logger.error(f"Error parsing entries: {str(e)}")
            logger.error(f"Content preview causing error: {content[:500]}")
            raise Exception(f"Entry parsing failed: {str(e)}") 