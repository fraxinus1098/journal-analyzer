"""
Service for parsing and segmenting journal entries.
"""
import re
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class EntryParser:
    def __init__(self):
        # Regex for MM/DD/YYYY format - made more flexible
        self.date_pattern = r'\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/([12]\d{3})\b'
    
    def parse_entries(self, content: str, source_file: str) -> List[dict]:
        """Parse content into separate journal entries."""
        try:
            # Ensure content is string
            if not isinstance(content, str):
                raise ValueError(f"Expected string content, got {type(content)}")
            
            # Debug: Print first 100 characters of content
            logger.info(f"Content preview: {content[:100]}")
            
            # Find all dates in the content
            dates = re.finditer(self.date_pattern, content)
            date_positions = [(m.group(0), m.start()) for m in dates]
            
            if not date_positions:
                raise ValueError("No dates found in the content")
            
            entries = []
            entry_number = 1
            
            # Process entries using date positions
            for i in range(len(date_positions)):
                current_date_str, current_pos = date_positions[i]
                
                # Get content until next date or end of file
                if i < len(date_positions) - 1:
                    next_pos = date_positions[i + 1][1]
                    entry_content = content[current_pos + len(current_date_str):next_pos].strip()
                else:
                    entry_content = content[current_pos + len(current_date_str):].strip()
                
                if not entry_content:  # Skip empty entries
                    continue
                
                try:
                    # Parse date components
                    date = datetime.strptime(current_date_str, '%m/%d/%Y').date()
                    
                    # Create entry
                    entry = {
                        'date': date,
                        'content': entry_content,
                        'word_count': len(entry_content.split()),
                        'year': date.year,
                        'month': date.month,
                        'day': date.day,
                        'source_file': source_file,
                        'entry_number': entry_number,
                        'sentiment_score': None,
                        'complexity_score': None,
                        'topics': None,
                        'mentioned_people': None,
                        'mentioned_locations': None,
                        'embedding': None
                    }
                    
                    entries.append(entry)
                    entry_number += 1
                    
                except ValueError as e:
                    logger.warning(f"Skipping entry with invalid date {current_date_str}: {str(e)}")
                    continue
            
            if not entries:
                raise ValueError("No valid entries were parsed")
            
            logger.info(f"Successfully parsed {len(entries)} entries from {source_file}")
            return entries
            
        except Exception as e:
            logger.error(f"Error parsing entries: {str(e)}")
            logger.error(f"Content preview causing error: {content[:500]}")
            raise Exception(f"Entry parsing failed: {str(e)}") 