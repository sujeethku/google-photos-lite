from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def extract_exif(file_path: str) -> dict:
    exif_data = {
        "taken_at": None,
        "camera_make": None,
        "camera_model": None,
        "width": None,
        "height": None,
        "orientation": None,
    }

    try:
        image = Image.open(file_path)
        exif_raw = image._getexif()

        exif_data["width"], exif_data["height"] = image.size

        if not exif_raw:
            return exif_data

        for tag_id, value in exif_raw.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTimeOriginal":
                try:
                    exif_data["taken_at"] = datetime.strptime(
                        value, "%Y:%m:%d %H:%M:%S"
                    ).isoformat()
                except Exception:
                    pass

            elif tag == "Make":
                exif_data["camera_make"] = value

            elif tag == "Model":
                exif_data["camera_model"] = value

            elif tag == "Orientation":
                exif_data["orientation"] = value

    except Exception:
        # EXIF failures should NEVER break upload
        return exif_data

    return exif_data
