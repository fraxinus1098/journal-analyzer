import re
from typing import Optional

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    
    # Remove any PDF artifacts or control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove multiple newlines while preserving paragraph breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove table artifacts (common in PDFs)
    text = re.sub(r'[|┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬]', '', text)
    
    # Remove image references and captions
    text = re.sub(r'\[Image:.*?\]', '', text, flags=re.DOTALL)
    text = re.sub(r'Figure \d+:.*?\n', '', text)
    
    # Clean up whitespace
    text = text.strip()
    
    return text 