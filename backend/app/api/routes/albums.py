from fastapi import APIRouter

router = APIRouter()

@router.post("/albums")
def create_album(name: str):
    return {"message": f"album created (scaffold): {name}"}

@router.get("/albums")
def list_albums():
    return {"message": "albums list scaffold"}

@router.post("/albums/{album_id}/add")
def add_to_album(album_id: str, photo_ids: list[str] = []):
    return {"message": f"photos added scaffold to album {album_id}"}
