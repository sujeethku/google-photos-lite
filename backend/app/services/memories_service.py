MAX_PHOTOS_PER_MEMORY = 5

from datetime import datetime, timedelta
from typing import List, Dict

from app.services.local_photos_service import list_local_photos


# ---------- helpers ----------

from datetime import datetime

def _parse_photo_timestamp(photo: dict) -> datetime:
    exif = photo.get("exif", {})

    # 1️⃣ Preferred: normalized EXIF
    taken_at = exif.get("taken_at")
    if taken_at:
        try:
            return datetime.fromisoformat(taken_at)
        except Exception:
            pass

    # 2️⃣ Fallback: filesystem timestamp
    uploaded_at = photo.get("uploaded_at")
    if uploaded_at:
        try:
            return datetime.fromisoformat(uploaded_at)
        except Exception:
            pass

    return datetime.min


def compute_quality_score(photo: dict) -> float:
    exif = photo.get("exif", {})

    # Resolution score
    try:
        width = int(exif.get("ExifImageWidth", 0))
        height = int(exif.get("ExifImageHeight", 0))
        resolution_score = (width * height) / 1_000_000
    except Exception:
        resolution_score = 0.5

    # Orientation penalty
    orientation = exif.get("Orientation")
    orientation_penalty = 0.3 if orientation not in (None, "1", 1) else 0.0

    # Recency score
    ts = _parse_photo_timestamp(photo)
    recency_score = ts.timestamp() / 1e10 if ts != datetime.min else 0

    return resolution_score + recency_score - orientation_penalty

# ---------- memory generation ----------

def generate_time_based_memories(photos: list) -> List[Dict]:
    """
    Generates simple time-based memories:
    - Today
    - This Week
    - This Month

    Applies quality ranking before selecting photos.
    """

    photos = list_local_photos()
    now = datetime.now()

    buckets = {
        "Today": [],
        "This Week": [],
        "This Month": [],
    }

    # bucket photos by time
    for photo in photos:
        ts = _parse_photo_timestamp(photo)

        if ts.date() == now.date():
            buckets["Today"].append(photo)
        elif ts >= now - timedelta(days=7):
            buckets["This Week"].append(photo)
        elif ts >= now - timedelta(days=30):
            buckets["This Month"].append(photo)

    memories = []

    for title, items in buckets.items():
        if not items:
            continue

        # 1️⃣ Rank by quality (deterministic)
        ranked_items = sorted(
            items,
            key=lambda p: compute_quality_score(p),
            reverse=True
        )

        # 2️⃣ Cap number of photos
        top_photos = ranked_items[:MAX_PHOTOS_PER_MEMORY]

        # 3️⃣ Explicit best cover selection
        cover_photo = top_photos[0]

        memories.append({
            "title": title,
            "photo_count": len(top_photos),
            "cover_photo_id": cover_photo["id"],
            "photos": top_photos
        })

    return memories
