from pathlib import Path
import pdfplumber
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import re
from ..models.journal import JournalEntry
from ..db.session import get_db
from ..utils.text_cleaner import clean_text
import logging
from ..services.entry_parser import EntryParser
from ..services.validation_service import ValidationService
from ..services.storage_service import StorageService
from ..config import settings

logger = logging.getLogger(__name__)

class PDFService:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
        
    def process_pdf(self, file_path: Path, original_filename: str) -> str:
        """Process a PDF file and extract journal entries"""
        task_id = f"task_{original_filename}_{datetime.now().timestamp()}"
        self._tasks[task_id] = {"status": "processing", "progress": 0}
        
        try:
            raw_text = ""
            with pdfplumber.open(file_path) as pdf:
                total_pages = len(pdf.pages)
                
                for i, page in enumerate(pdf.pages):
                    # Extract text with optimal settings
                    text = page.extract_text(
                        x_tolerance=3,
                        y_tolerance=3,
                        layout=False,
                        x_density=7.25,
                        y_density=13
                    )
                    raw_text += text + "\n"
                    
                    # Update progress
                    self._tasks[task_id]["progress"] = (i + 1) / total_pages * 50  # First 50%
                
            # Parse entries
            parser = EntryParser()
            entries = parser.parse_entries(raw_text)
            
            # Update progress
            self._tasks[task_id]["progress"] = 75  # 75% after parsing
            
            # Add validation step
            validator = ValidationService()
            validated_entries = self._clean_and_validate_entries(entries)
            
            # Update progress and store validation results
            self._tasks[task_id].update({
                "total_entries": len(entries),
                "valid_entries": len(validated_entries),
                "validation_errors": validator.get_validation_errors()
            })
            
            # Store only validated entries
            self._store_entries(validated_entries)
            
            self._tasks[task_id].update({
                "status": "completed",
                "message": f"Successfully processed {len(validated_entries)} valid entries"
            })
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            self._tasks[task_id].update({
                "status": "error",
                "error": str(e)
            })
            raise
            
        finally:
            # Cleanup temporary file
            file_path.unlink(missing_ok=True)
            
        return task_id
    
    def _process_page_text(
        self, 
        text: str, 
        current_entry: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Process text from a page and extract entries"""
        entries = []
        date_pattern = r"(\d{2}/\d{2}/\d{4})(.*?)(?=\d{2}/\d{2}/\d{4}|$)"
        matches = re.finditer(date_pattern, text, re.DOTALL)
        
        for match in matches:
            date_str, content = match.groups()
            try:
                date = datetime.strptime(date_str.strip(), "%m/%d/%Y")
                
                # Clean the text with better tolerance settings
                cleaned_content = content.strip()
                if cleaned_content:
                    entries.append({
                        "date": date,
                        "content": cleaned_content,
                        "year": date.year,
                        "month": date.month,
                        "day": date.day,
                        "word_count": len(cleaned_content.split())
                    })
            except ValueError as e:
                logger.warning(f"Invalid date format: {date_str}", exc_info=True)
                continue
                
        return entries
    
    def _clean_and_validate_entries(
        self, 
        entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Clean and validate journal entries"""
        cleaned_entries = []
        
        for entry in entries:
            # Skip empty entries
            if not entry["content"].strip():
                continue
                
            # Clean the text content
            cleaned_content = clean_text(entry["content"])
            
            # Validate entry
            if self._validate_entry(cleaned_content, entry["date"]):
                entry["content"] = cleaned_content
                cleaned_entries.append(entry)
        
        # Sort entries by date
        cleaned_entries.sort(key=lambda x: x["date"])
        
        return cleaned_entries
    
    def _validate_entry(self, content: str, date: datetime) -> bool:
        """Validate a journal entry"""
        # Check for minimum content length
        if len(content.strip()) < 10:
            return False
            
        # Check if date is within valid range (2019-2024)
        if not (2019 <= date.year <= 2024):
            return False
            
        return True
    
    def _store_entries(self, entries: List[JournalEntry]) -> Dict[str, Any]:
        """Store validated entries"""
        try:
            storage = StorageService(settings.DATABASE_URL)
            result = storage.store_entries(entries)
            
            # Optimize storage if needed
            if result["stored_entries"] > 1000:  # threshold for optimization
                storage.optimize_storage()
            
            return result
            
        except Exception as e:
            logger.error(f"Error storing entries: {str(e)}", exc_info=True)
            raise 