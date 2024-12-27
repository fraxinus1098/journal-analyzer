import requests
from pathlib import Path

def upload_pdfs(pdf_files, base_url):
    """Upload PDFs to Replit instance"""
    url = f"{base_url}/api/upload/"
    files = [
        ('files', (f.name, open(f, 'rb'), 'application/pdf'))
        for f in pdf_files
    ]
    response = requests.post(url, files=files)
    return response.json()

if __name__ == "__main__":
    import sys
    
    # Your Replit URL
    REPLIT_URL = "https://your-repl-name.your-username.repl.co"
    
    if len(sys.argv) < 2:
        print("Usage: python upload_pdfs.py <pdf_file1> [pdf_file2 ...]")
        sys.exit(1)
    
    pdf_files = [Path(f) for f in sys.argv[1:]]
    result = upload_pdfs(pdf_files, REPLIT_URL)
    print(result) 