"""
Service for validating journal entries.
"""
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataValidator:
    def validate_entries(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate journal entries."""
        valid_entries = []
        
        logger.info(f"Starting validation of {len(entries)} entries")
        
        for entry in entries:
            try:
                # Log the entry being validated
                logger.info(f"Validating entry: {entry.get('date')} - {entry.get('content')[:50]}...")
                
                # Validate required fields exist
                required_fields = ['date', 'content', 'source_file']
                missing_fields = [field for field in required_fields if field not in entry]
                if missing_fields:
                    logger.warning(f"Entry missing required fields: {missing_fields}")
                    continue
                
                # Validate content is not empty
                if not entry['content'] or not entry['content'].strip():
                    logger.warning("Entry has empty content")
                    continue
                
                # More lenient date validation
                if not entry['date']:
                    logger.warning(f"Invalid date: {entry.get('date')}")
                    continue
                
                # More lenient word count validation
                if 'word_count' not in entry or entry['word_count'] is None:
                    entry['word_count'] = len(entry['content'].split())
                    logger.info(f"Added word count: {entry['word_count']}")
                
                valid_entries.append(entry)
                logger.info(f"Entry validated successfully: {entry.get('date')}")
                
            except Exception as e:
                logger.error(f"Error validating entry: {str(e)}")
                continue
        
        logger.info(f"Validation complete. {len(valid_entries)} valid out of {len(entries)} total")
        return valid_entries 