from collections import Counter
from app.services.memories_service import generate_time_based_memories
from datetime import datetime




def generate_narratives():
    memories = generate_time_based_memories([])

    narratives = []

    for memory in memories:
        photos = memory["photos"]
        exifs = [p.get("exif", {}) for p in photos]

        camera_models = [
            e.get("Model") for e in exifs if e.get("Model")
        ]

        model_summary = ""
        if camera_models:
            common_model = Counter(camera_models).most_common(1)[0][0]
            model_summary = f" using your {common_model}"

        narrative_text = (
            f"You captured {memory['photo_count']} photos "
            f"during {memory['title'].lower()}{model_summary}."
        )

        narratives.append({
            "memory_title": memory["title"],
            "narrative": narrative_text
        })

    return narratives

def generate_search_narrative(photos, from_date=None, to_date=None):
    if not photos:
        return "No moments found for this time period."

    exifs = [p.get("exif", {}) for p in photos]

    camera_models = [
        e.get("camera_model") for e in exifs if e.get("camera_model")
    ]

    camera_text = ""
    if camera_models:
        camera_text = f" captured on my {camera_models[0]}"

    date_text = ""
    if from_date and to_date:
        date_text = f" from {from_date} to {to_date}"

    # NOTE:
        # This narrative is intentionally rule-based and hardcoded for V1.
        # The goal is to demonstrate end-to-end product thinking and UX flow,
        # not model sophistication.
        #
        # V2 will replace this with:
        # - Vision API / multimodal model integration
        # - Pixel-level understanding (faces, scenes, objects, expressions)
        # - Learned ranking + narrative generation based on visual semantics

    return (
        f"Some of my favorite moments{date_text}{camera_text}. "
        f"Simple days, great memories 📸✨"
    )

"""
V1 NOTE:
This narrative generation is intentionally rule-based and EXIF-driven.
In V2, this will be replaced by Vision / multimodal models that analyze
pixels, objects, and scenes directly.
"""

def generate_search_narrative(photos: list, query: str = None) -> str:
    if not photos:
        return "A few moments captured."

    exifs = [p.get("exif", {}) for p in photos]

    # Camera summary
    models = [e.get("camera_model") for e in exifs if e.get("camera_model")]
    camera = Counter(models).most_common(1)[0][0] if models else None

    # Time summary
    dates = [
        e.get("taken_at") for e in exifs if e.get("taken_at")
    ]
    month = None
    if dates:
        dt = datetime.fromisoformat(dates[0])
        month = dt.strftime("%B")

    parts = []

    # --- Narrative construction ---

    if query and month:
        summary = f"Peaceful moments in nature from {month}"
    elif query:
        summary = "Peaceful moments in nature"
    elif month:
        summary = f"Memories from {month}"
    else:
        summary = "A few moments captured"

    camera_text = f" on my {camera}" if camera else ""

    return f"{summary}, captured{camera_text} 🌊✨"
