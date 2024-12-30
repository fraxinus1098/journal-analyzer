"""
Service for processing PDF files using PDFPlumber.
"""
import pdfplumber
from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.current_file: Path | None = None
        
    async def process_pdf(self, file_path: str | Path) -> List[Dict[str, Any]]:
        """
        Process a PDF file and extract text with positioning information.
        Returns a list of dictionaries containing page content and metadata.
        """
        self.current_file = Path(file_path)
        extracted_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text with positioning
                    text = page.extract_text()
                    words = page.extract_words()
                    
                    page_content = {
                        'page_number': page_num,
                        'text': text,
                        'words': words,
                        'metadata': {
                            'page_size': page.size,
                            'rotation': page.rotation,
                        }
                    }
                    extracted_content.append(page_content)
                    
            return extracted_content
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise 