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

logger = logging.getLogger(__name__)
router = APIRouter()

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
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Create processing status
    status = ProcessingStatus()
    
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
    # In a production environment, you'd want to store this in Redis or similar
    status = ProcessingStatus.get(status_id)
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
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            status.progress = 10
            
            # Process PDF
            extracted_content = await pdf_processor.process_pdf(temp_file.name)
            status.progress = 30
            
            # Parse entries
            entries = entry_parser.parse_entries(extracted_content)
            status.progress = 50
            
            # Clean entries
            cleaned_entries = [
                JournalEntrySchema(
                    **{**entry.dict(),
                       "content": data_cleaner.clean_text(entry.content)}
                )
                for entry in entries
            ]
            status.progress = 70
            
            # Validate entries
            valid_entries = data_validator.validate_entries(cleaned_entries)
            status.progress = 80
            
            # Store entries
            success_count, errors = await db_operations.store_entries(valid_entries)
            
            # Update status
            status.status = "completed"
            status.progress = 100
            status.success_count = success_count
            status.errors.extend(errors)
            
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        status.status = "failed"
        status.errors.append(str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        if 'temp_file' in locals():
            os.unlink(temp_file.name) 