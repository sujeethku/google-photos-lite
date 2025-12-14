import os
import uuid
from datetime import datetime
from typing import List, Dict

from app.utils.exif_utils import extract_exif

# ----------------------------
# Config
# ----------------------------

LOCAL_PHOTOS_DIR = "/Users/sujeethkumartuniki/Pictures/Mypicslite"

# Simple in-memory cache for EXIF
IN_MEMORY_PHOTO_METADATA: Dict[str, Dict] = {}


# ----------------------------
# Ingestion (Local Folder)
# ----------------------------

def ingest_local_folder():
    """
    Reads photos from local folder and prepares metadata.
    This does NOT upload files — it indexes them.
    """

    if not os.path.exists(LOCAL_PHOTOS_DIR):
        return {"error": "Local photos folder not found"}

    ingested = []

    for filename in os.listdir(LOCAL_PHOTOS_DIR):
        file_path = os.path.join(LOCAL_PHOTOS_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        file_id = str(uuid.uuid4())

        exif_data = extract_exif(file_path)

        IN_MEMORY_PHOTO_METADATA[file_id] = {
            "stored_filename": filename,
            "exif": exif_data,
            "indexed_at": datetime.now().isoformat(),
        }

        ingested.append({
            "id": file_id,
            "stored_filename": filename,
            "exif": exif_data
        })

    return {
        "ingested_count": len(ingested),
        "files": ingested
    }


# ----------------------------
# Read API (Photos & Memories)
# ----------------------------

def list_local_photos() -> List[Dict]:
    """
    Single source of truth for Photos, Memories, Search.
    """

    photos = []

    if not os.path.exists(LOCAL_PHOTOS_DIR):
        return photos

    for filename in os.listdir(LOCAL_PHOTOS_DIR):
        file_path = os.path.join(LOCAL_PHOTOS_DIR, filename)

        if not os.path.isfile(file_path):
            continue

        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        stat = os.stat(file_path)

        # Stable ID per filename (good enough for V1)
        file_id = filename

        metadata = IN_MEMORY_PHOTO_METADATA.get(file_id)

        if not metadata:
            exif_data = extract_exif(file_path)
            metadata = {"exif": exif_data}
            IN_MEMORY_PHOTO_METADATA[file_id] = metadata

        photos.append({
            "id": file_id,
            "stored_filename": filename,
            "size_bytes": stat.st_size,
            "uploaded_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "exif": metadata.get("exif", {})
        })

    return photos
