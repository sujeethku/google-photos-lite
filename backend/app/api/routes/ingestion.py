from fastapi import APIRouter
from app.services.local_photos_service import list_local_photos

router = APIRouter()

@router.post("/ingest-local")
def ingest_local():
    """
    Trigger ingestion from local folder (Mypicslite)
    """
    return list_local_photos()
