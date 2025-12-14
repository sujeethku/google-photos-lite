from fastapi import APIRouter
from app.services.local_photos_service import list_local_photos

router = APIRouter()

@router.get("/photos")
def get_photos():
    """
    Returns list of uploaded photos.
    """
    photos = list_local_photos()
    return {
        "count": len(photos),
        "photos": photos
    }
