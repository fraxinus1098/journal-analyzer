from fastapi import UploadFile
from typing import List

def validate_file_type(file: UploadFile, allowed_types: List[str]) -> bool:
    """
    Validate that the uploaded file is of an allowed type
    
    Args:
        file: The uploaded file
        allowed_types: List of allowed MIME types (e.g., ["application/pdf"])
    
    Returns:
        bool: True if file type is allowed, False otherwise
    """
    return file.content_type in allowed_types 