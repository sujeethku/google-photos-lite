import os
from typing import List
from fastapi import UploadFile
import uuid

UPLOAD_DIR = "backend/storage/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def process_uploaded_files(files: List[UploadFile]):
    """
    Step 1 of ingestion pipeline:
    - Validate files
    - Save raw files locally
    """
    saved_files = []

    for file in files:
        if not file.content_type.startswith("image/"):
            continue

        file_extension = file.filename.split(".")[-1]
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.{file_extension}")

        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        saved_files.append({
            "id": file_id,
            "original_filename": file.filename,
            "stored_path": file_path
        })

    return {
        "uploaded_count": len(saved_files),
        "files": saved_files
    }
