"""
Service for cleaning and normalizing text data.
"""
import re
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.pdf_artifacts = [
            r'\f',  # Form feed
            r'\x0c',  # Form feed
            r'^\s*Page\s+\d+\s*$',  # Page numbers
            r'^\s*\d+\s*$',  # Standalone numbers
        ]
        
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text content.
        """
        # Remove PDF artifacts
        for artifact in self.pdf_artifacts:
            text = re.sub(artifact, '', text, flags=re.MULTILINE)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        # Handle special characters
        text = self._handle_special_chars(text)
        
        # Remove table artifacts
        text = self._remove_table_artifacts(text)
        
        return text.strip()
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize various types of whitespace.
        """
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize line endings
        text = re.sub(r'\r\n|\r|\n', '\n', text)
        
        # Remove spaces before punctuation
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        
        return text
    
    def _handle_special_chars(self, text: str) -> str:
        """
        Handle special characters and encodings.
        """
        # Replace common special characters
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '…': '...',
            '–': '-',
            '—': '-'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        return text
    
    def _remove_table_artifacts(self, text: str) -> str:
        """
        Remove common table artifacts from text.
        """
        # Remove repeated dashes or underscores
        text = re.sub(r'[-_]{3,}', '', text)
        
        # Remove table borders
        text = re.sub(r'[|+]\s*[|+]', '', text)
        
        return text
    
    def clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize metadata.
        """
        cleaned = {}
        
        for key, value in metadata.items():
            # Convert keys to snake_case
            key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
            
            # Clean string values
            if isinstance(value, str):
                value = self.clean_text(value)
            
            cleaned[key] = value
            
        return cleaned 