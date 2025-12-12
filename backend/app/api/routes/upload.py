from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/upload")
async def upload_photos(files: List[UploadFile] = File(...)):
    """
    Uploads one or multiple photos.
    Full logic will be implemented in ingestion_service.
    """
    return {"message": "upload endpoint scaffold"}
