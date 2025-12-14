INTENT_KEYWORDS = {
    "beach": ["beach", "sea", "ocean", "sand", "wave"],
    "nature": ["nature", "tree", "forest", "mountain", "park"],
    "baby": ["baby", "kid", "child", "infant"],
    "food": ["food", "meal", "lunch", "dinner"]
}

from datetime import datetime
from typing import Optional, List

from app.services.local_photos_service import list_local_photos
from app.services.memories_service import compute_quality_score, _parse_photo_timestamp
from app.services.narrative_service import generate_search_narrative

def search_photos(
    query: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    limit: int = 5
):
    """
    Search photos by date range + optional text query,
    then rank by quality and return top N.
    """

    photos = list_local_photos()
    results = []

    # --- Parse dates ---
    start_dt = (
        datetime.fromisoformat(from_date)
        if from_date else None
    )
    end_dt = (
        datetime.fromisoformat(to_date)
        if to_date else None
    )

    for photo in photos:
        ts = _parse_photo_timestamp(photo)

        # 1️⃣ Date filtering
        if start_dt and ts < start_dt:
            continue
        if end_dt and ts > end_dt:
            continue

        # 2️⃣ Text query (V1 = filename only)
        if query:
            filename = photo.get("stored_filename", "").lower()
            q = query.lower()

            keywords = INTENT_KEYWORDS.get(q, [q])

            if not any(k in filename for k in keywords):
                continue

        results.append(photo)

    # 3️⃣ Quality ranking
    ranked = sorted(
        results,
        key=lambda p: compute_quality_score(p),
        reverse=True
    )

    # 4️⃣ Limit results
    top_photos = ranked[:limit]

    narrative = generate_search_narrative(
    photos=top_photos,
    query=query
    )

    return {
    "count": len(top_photos),
    "photos": top_photos,
    "narrative": narrative
    }


