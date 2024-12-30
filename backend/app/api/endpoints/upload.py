from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from typing import List
from pathlib import Path
import logging
from ...services.pdf_service import PDFService
from ...db.init_db import get_db
from ...models.journal import JournalEntry
from sqlalchemy.orm import Session

router = APIRouter()
pdf_service = PDFService()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """Upload and process PDF journal files"""
    results = []
    
    for file in files:
        try:
            # Validate and save file
            temp_file = UPLOAD_DIR / f"temp_{file.filename}"
            with temp_file.open("wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process PDF and get task_id
            task_id = pdf_service.process_pdf(temp_file, file.filename)
            
            # Get processed content
            status = pdf_service.get_task_status(task_id)
            if status["status"] == "completed":
                # Create journal entry with only valid fields
                journal_entry = JournalEntry(
                    content=status["result"],
                    filename=file.filename
                )
                db.add(journal_entry)
                db.commit()
            
            results.append({
                "filename": file.filename,
                "task_id": task_id,
                "status": status["status"]
            })
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })
            
    return JSONResponse(content={"results": results})

@router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str) -> JSONResponse:
    """Get the status of a file upload/processing task"""
    status = pdf_service.get_task_status(task_id)
    if status["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(content=status)

@router.get("/entries/")
def get_entries(db: Session = Depends(get_db)):
    """Get all journal entries"""
    try:
        entries = db.query(JournalEntry).all()
        return {
            "total": len(entries),
            "entries": [
                {
                    "id": entry.id,
                    "content": entry.content[:100] + "...",  # Preview only
                    "created_at": entry.created_at
                }
                for entry in entries
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch entries: {str(e)}"
        ) 