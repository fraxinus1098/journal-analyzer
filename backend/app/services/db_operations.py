"""
Service for handling database operations with batch processing and error handling.
"""
from sqlalchemy.orm import Session
from typing import List, Tuple, Dict, Any
from ..models.journal import JournalEntry
import logging

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self, db: Session):
        self.db = db
    
    async def store_entries(self, entries: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
        """Store journal entries in the database."""
        success_count = 0
        errors = []
        
        for entry_data in entries:
            try:
                # Create new JournalEntry instance
                db_entry = JournalEntry(
                    entry_date=entry_data['date'],
                    content=entry_data['content'],
                    word_count=entry_data['word_count'],
                    year=entry_data['year'],
                    month=entry_data['month'],
                    day=entry_data['day'],
                    source_file=entry_data['source_file'],
                    entry_number=entry_data['entry_number'],
                    sentiment_score=entry_data.get('sentiment_score'),
                    complexity_score=entry_data.get('complexity_score'),
                    topics=entry_data.get('topics'),
                    mentioned_people=entry_data.get('mentioned_people'),
                    mentioned_locations=entry_data.get('mentioned_locations'),
                    embedding=entry_data.get('embedding')
                )
                
                # Add and commit
                self.db.add(db_entry)
                self.db.commit()
                self.db.refresh(db_entry)
                
                success_count += 1
                logger.info(f"Successfully stored entry {success_count} for date {entry_data['date']}")
                
            except Exception as e:
                self.db.rollback()
                error_msg = f"Error storing entry for date {entry_data.get('date', 'unknown')}: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                continue
        
        logger.info(f"Completed storing entries. Success: {success_count}, Errors: {len(errors)}")
        return success_count, errors 