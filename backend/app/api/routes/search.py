from fastapi import APIRouter, Query
from typing import Optional
from app.services.search_service import search_photos

router = APIRouter()

@router.get("/search")
def search(
    q: Optional[str] = Query(None, description="Search intent (e.g. beach, baby)"),
    from_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    to_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    limit: int = Query(5, description="Top N photos")
):
    return search_photos(
        query=q,
        from_date=from_date,
        to_date=to_date,
        limit=limit
    )
