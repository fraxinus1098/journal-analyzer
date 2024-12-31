"""
Service for processing PDF files using PDFPlumber.
"""
import pdfplumber
from pathlib import Path
from typing import List, Dict, Any, Union, Optional
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.current_file: Optional[Path] = None
        
    async def process_pdf(self, file_path: str) -> str:
        """
        Process PDF file and return extracted text content.
        Returns a single string with all content.
        """
        try:
            logger.info(f"Opening PDF: {file_path}")
            text_content = []
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            
            # Join all pages with newlines
            full_text = "\n".join(text_content)
            logger.info(f"Successfully extracted {len(text_content)} pages of text")
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}") 