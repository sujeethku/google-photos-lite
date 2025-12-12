from fastapi import APIRouter, UploadFile, File
from typing import List

from app.services.ingestion_service import process_uploaded_files

router = APIRouter()

@router.post("/upload")
async def upload_photos(files: List[UploadFile] = File(...)):
    """
    Upload one or more photos and trigger ingestion pipeline.
    """
    result = await process_uploaded_files(files)
    return result
