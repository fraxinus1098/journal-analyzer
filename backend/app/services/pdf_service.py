from pdfplumber import open as pdf_open
from typing import Dict, Any
import uuid
from pathlib import Path

class PDFService:
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def process_pdf(self, file_path: Path, filename: str) -> str:
        """Process PDF and return task_id"""
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = {
            "status": "processing",
            "filename": filename,
            "result": None,
            "error": None
        }

        try:
            with pdf_open(file_path) as pdf:
                text_content = ""
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
                
                self._tasks[task_id].update({
                    "status": "completed",
                    "result": text_content
                })
                return task_id

        except Exception as e:
            self._tasks[task_id].update({
                "status": "failed",
                "error": str(e)
            })
            raise

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a processing task"""
        if task_id not in self._tasks:
            return {"status": "not_found"}
        return self._tasks[task_id] 