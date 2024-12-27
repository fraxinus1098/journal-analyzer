from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import os
import shutil
from pathlib import Path
import re
import logging
from ...services.pdf_service import PDFService
from ...core.config import settings
from ...utils.security import validate_file_type
import requests

router = APIRouter()
pdf_service = PDFService()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal"""
    # Remove any directory components
    filename = Path(filename).name
    # Remove any non-alphanumeric chars except for periods and underscores
    filename = re.sub(r'[^\w\-_\.]', '_', filename)
    return filename

@router.post("/upload/")
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
) -> JSONResponse:
    """
    Upload and process PDF journal files
    
    Args:
        background_tasks: FastAPI BackgroundTasks instance
        files: List of files to upload
        
    Returns:
        JSONResponse with upload results
    """
    results = []
    temp_files = []  # Track temp files for cleanup
    
    for file in files:
        temp_file = None
        try:
            # Validate file type using the imported utility
            if not validate_file_type(file, allowed_types=["application/pdf"]):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # Validate file size
            file_size = 0
            chunk_size = 8192  # 8KB chunks
            
            # Create temporary file path with sanitized name
            safe_filename = sanitize_filename(file.filename)
            temp_file = UPLOAD_DIR / f"temp_{safe_filename}"
            temp_files.append(temp_file)
            
            # Save and validate file size
            try:
                with temp_file.open("wb") as buffer:
                    while chunk := await file.read(chunk_size):
                        file_size += len(chunk)
                        if file_size > MAX_FILE_SIZE:
                            raise HTTPException(
                                status_code=400, 
                                detail=f"File size exceeds {MAX_FILE_SIZE // 1024 // 1024}MB limit"
                            )
                        buffer.write(chunk)
            except OSError as e:
                raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
            
            # Add to background processing queue
            background_tasks.add_task(
                pdf_service.process_pdf,
                temp_file,
                safe_filename
            )
            
            results.append({
                "filename": safe_filename,
                "status": "processing",
                "message": "File uploaded and queued for processing"
            })
            
        except HTTPException as e:
            # Re-raise HTTP exceptions
            raise e
        except Exception as e:
            logger.error(f"Error processing file {getattr(file, 'filename', 'unknown')}: {str(e)}")
            # Clean up temp file if it exists
            if temp_file and temp_file.exists():
                temp_file.unlink()
                
            results.append({
                "filename": getattr(file, 'filename', 'unknown'),
                "status": "error",
                "message": str(e)
            })
            
        finally:
            await file.close()
    
    # Add cleanup task for successful uploads
    background_tasks.add_task(cleanup_temp_files, temp_files)
            
    return JSONResponse(content={"results": results})

async def cleanup_temp_files(temp_files: List[Path]) -> None:
    """
    Clean up temporary files after processing
    
    Args:
        temp_files: List of temporary file paths to clean up
    """
    for temp_file in temp_files:
        try:
            if temp_file.exists():
                temp_file.unlink()
        except OSError as e:
            logger.error(f"Error cleaning up {temp_file}: {e}")

@router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str) -> JSONResponse:
    """
    Get the status of a file upload/processing task
    
    Args:
        task_id: ID of the upload task to check
        
    Returns:
        JSONResponse with task status
    """
    status = pdf_service.get_task_status(task_id)
    return JSONResponse(content=status) 

def upload_pdfs(pdf_files):
    url = "http://localhost:8000/api/upload/"
    files = [
        ('files', (f.name, open(f, 'rb'), 'application/pdf'))
        for f in pdf_files
    ]
    response = requests.post(url, files=files)
    return response.json()

# Example usage:
pdfs = [
    "path/to/2019.pdf",
    "path/to/2020.pdf",
    # ... add more files as needed
]
result = upload_pdfs(pdfs)
print(result) 