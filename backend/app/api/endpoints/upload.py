"""
API endpoint for file uploads and processing.
"""
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import tempfile
import os
from ...services.pdf_processor import PDFProcessor
from ...services.entry_parser import EntryParser
from ...services.data_cleaner import DataCleaner
from ...services.data_validator import DataValidator
from ...services.db_operations import DatabaseOperations
from ...db.init_db import get_db
from ...models.journal import JournalEntrySchema
import logging
from ...services.status_manager import StatusManager
from ...core.config import settings
import traceback

logger = logging.getLogger(__name__)
router = APIRouter()

# Add size limit (e.g., 50MB)
MAX_FILE_SIZE = 52_428_800  # 50MB in bytes

class ProcessingStatus:
    def __init__(self):
        self.status = "processing"
        self.progress = 0
        self.errors = []
        self.success_count = 0

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Handle file upload and processing.
    """
    # Check file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end of file
    file_size = file.file.tell()  # Get current position (file size)
    file.file.seek(0)  # Reset position to start
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE // 1_048_576}MB"
        )
    
    # Create processing status using StatusManager
    status = StatusManager.create()
    
    # Add processing task to background
    background_tasks.add_task(
        process_file,
        file,
        status,
        db
    )
    
    return {"message": "Processing started", "status_id": id(status)}

@router.get("/status/{status_id}")
async def get_status(status_id: int):
    """
    Get the current processing status.
    """
    status = StatusManager.get(status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    
    return {
        "status": status.status,
        "progress": status.progress,
        "errors": status.errors,
        "success_count": status.success_count
    }

async def process_file(file: UploadFile, status: ProcessingStatus, db: Session):
    """
    Process the uploaded file using our pipeline.
    """
    # Initialize services
    pdf_processor = PDFProcessor()
    entry_parser = EntryParser()
    data_cleaner = DataCleaner()
    data_validator = DataValidator()
    db_operations = DatabaseOperations(db)
    
    try:
        logger.info(f"Starting to process file: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            logger.info(f"Saved temporary file: {temp_file.name}")
            status.progress = 10
            
            # Process PDF
            logger.info("Starting PDF processing")
            extracted_content = await pdf_processor.process_pdf(temp_file.name)
            logger.info(f"PDF processing complete. Extracted {len(extracted_content)} pages")
            status.progress = 30
            
            # Parse entries
            logger.info("Starting entry parsing")
            entries = entry_parser.parse_entries(extracted_content)
            logger.info(f"Entry parsing complete. Found {len(entries)} entries")
            status.progress = 50
            
            # Clean entries
            logger.info("Starting data cleaning")
            cleaned_entries = [
                JournalEntrySchema(
                    **{**entry.dict(),
                       "content": data_cleaner.clean_text(entry.content)}
                )
                for entry in entries
            ]
            logger.info(f"Data cleaning complete. Cleaned {len(cleaned_entries)} entries")
            status.progress = 70
            
            # Validate entries
            logger.info("Starting entry validation")
            valid_entries = data_validator.validate_entries(cleaned_entries)
            logger.info(f"Validation complete. {len(valid_entries)} valid entries")
            status.progress = 80
            
            # Store entries
            logger.info("Starting database storage")
            success_count, errors = await db_operations.store_entries(valid_entries)
            logger.info(f"Storage complete. Stored {success_count} entries with {len(errors)} errors")
            
            # Update status
            status.status = "completed"
            status.progress = 100
            status.success_count = success_count
            if errors:
                status.errors.extend(errors)
            
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        logger.error(traceback.format_exc())  # Log full traceback
        status.status = "failed"
        status.errors.append(str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
                logger.info(f"Cleaned up temporary file: {temp_file.name}")
            except Exception as e:
                logger.error(f"Error cleaning up temporary file: {str(e)}") 