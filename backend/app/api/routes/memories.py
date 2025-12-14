from fastapi import APIRouter
from app.services.local_photos_service import list_local_photos
from app.services.memories_service import generate_time_based_memories

router = APIRouter()

@router.get("/memories")
def list_memories():
    photos = list_local_photos()
    memories = generate_time_based_memories(photos)
    return memories


@router.get("/memories/{memory_id}")
def get_memory(memory_id: str):
    return {"message": f"memory detail scaffold {memory_id}"}
