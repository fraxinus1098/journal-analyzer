from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List
import os
import shutil
from pathlib import Path
from ...services.pdf_service import PDFService
from ...core.config import settings
from ...utils.security import validate_file_type

router = APIRouter()
pdf_service = PDFService()

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit

@router.post("/upload/")
async def upload_files(
    files: List[UploadFile] = File(...),
    background_tasks: BackgroundTasks
):
    """
    Upload and process PDF journal files
    """
    results = []
    
    for file in files:
        try:
            # Validate file type and size
            if not file.content_type == "application/pdf":
                raise HTTPException(400, "Only PDF files are allowed")
                
            # Create temporary file path
            temp_file = UPLOAD_DIR / f"temp_{file.filename}"
            
            # Save file to temporary location
            try:
                with temp_file.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
            finally:
                file.file.close()
            
            # Add to background processing queue
            background_tasks.add_task(
                pdf_service.process_pdf,
                temp_file,
                file.filename
            )
            
            results.append({
                "filename": file.filename,
                "status": "processing",
                "message": "File uploaded and queued for processing"
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
            
    return JSONResponse(content={"results": results})

@router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str):
    """
    Get the status of a file upload/processing task
    """
    status = pdf_service.get_task_status(task_id)
    return JSONResponse(content=status) 