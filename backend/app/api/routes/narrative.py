from fastapi import APIRouter
from app.services.narrative_service import generate_narratives

router = APIRouter()

@router.get("/narrative")
def get_narratives():
    return generate_narratives()
