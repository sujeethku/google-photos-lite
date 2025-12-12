from fastapi import APIRouter

router = APIRouter()

@router.get("/memories")
def list_memories():
    return {"message": "memories scaffold"}

@router.get("/memories/{memory_id}")
def get_memory(memory_id: str):
    return {"message": f"memory detail scaffold {memory_id}"}
