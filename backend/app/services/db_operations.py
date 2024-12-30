"""
Service for handling database operations with batch processing and error handling.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
import logging
from ..models.journal import JournalEntry, JournalEntrySchema
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseOperations:
    def __init__(self, db: Session):
        self.db = db
        self.batch_size = 100  # Adjust based on your needs
        
    async def store_entries(self, entries: List[JournalEntrySchema]) -> tuple[int, List[str]]:
        """
        Store multiple journal entries with batch processing.
        Returns tuple of (success_count, error_messages).
        """
        success_count = 0
        errors = []
        
        # Process entries in batches
        for i in range(0, len(entries), self.batch_size):
            batch = entries[i:i + self.batch_size]
            try:
                # Begin transaction for batch
                db_entries = [self._schema_to_db_model(entry) for entry in batch]
                self.db.add_all(db_entries)
                self.db.commit()
                success_count += len(batch)
                
            except SQLAlchemyError as e:
                self.db.rollback()
                error_msg = f"Batch {i//self.batch_size} failed: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
                
                # Try to save entries individually
                for entry in batch:
                    try:
                        self._store_single_entry(entry)
                        success_count += 1
                    except SQLAlchemyError as individual_error:
                        error_msg = f"Entry failed: {str(individual_error)}"
                        errors.append(error_msg)
                        logger.error(error_msg)
        
        return success_count, errors
    
    def _store_single_entry(self, entry: JournalEntrySchema) -> Optional[JournalEntry]:
        """
        Store a single journal entry with retry logic.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                db_entry = self._schema_to_db_model(entry)
                self.db.add(db_entry)
                self.db.commit()
                return db_entry
            except SQLAlchemyError as e:
                self.db.rollback()
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Retry attempt {attempt + 1} for entry {entry.date}")
        
        return None
    
    def _schema_to_db_model(self, entry: JournalEntrySchema) -> JournalEntry:
        """
        Convert a JournalEntrySchema to a database model.
        """
        return JournalEntry(
            content=entry.content,
            created_at=entry.date,
            updated_at=datetime.utcnow()
        ) 