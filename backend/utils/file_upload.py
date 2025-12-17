import os
from fastapi import UploadFile
import shutil
from pathlib import Path

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

def save_salary_slip(file: UploadFile, session_id: str) -> str:
    # Create session directory
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(exist_ok=True, parents=True)
    
    file_path = session_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return str(file_path)

def extract_salary_from_filename(filename: str) -> float:
    # Mock logic: extract number from filename (e.g., salary_50000.pdf -> 50000)
    try:
        # Simple heuristic: remove extension, split by underscore, find number
        name_part = Path(filename).stem
        parts = name_part.split('_')
        for part in parts:
            if part.isdigit():
                return float(part)
        return 0.0
    except Exception:
        return 0.0
