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
        
    async def process_pdf(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Process a PDF file and extract text with positioning information.
        Returns a list of dictionaries containing page content and metadata.
        """
        self.current_file = Path(file_path)
        extracted_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                logger.info(f"Processing PDF with {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.info(f"Processing page {page_num}")
                    
                    # Extract text with positioning
                    try:
                        text = page.extract_text() or ""
                        words = page.extract_words()
                        
                        # Get page dimensions from bbox instead of size
                        bbox = page.bbox
                        width = bbox[2] - bbox[0]
                        height = bbox[3] - bbox[1]
                        
                        page_content = {
                            'page_number': page_num,
                            'text': text,
                            'words': words,
                            'metadata': {
                                'width': width,
                                'height': height,
                                'rotation': page.rotation or 0,
                            }
                        }
                        extracted_content.append(page_content)
                        logger.info(f"Successfully processed page {page_num}")
                        
                    except Exception as page_error:
                        logger.error(f"Error processing page {page_num}: {str(page_error)}")
                        # Continue with next page instead of failing completely
                        continue
                    
            logger.info(f"Successfully processed PDF with {len(extracted_content)} pages")
            return extracted_content
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise 