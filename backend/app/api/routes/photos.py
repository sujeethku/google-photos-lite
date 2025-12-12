from fastapi import APIRouter

router = APIRouter()

@router.get("/photos")
def list_photos(page: int = 1, limit: int = 30):
    return {"message": "photos list scaffold"}

@router.get("/photos/{photo_id}")
def get_photo(photo_id: str):
    return {"message": f"photo detail scaffold for {photo_id}"}
