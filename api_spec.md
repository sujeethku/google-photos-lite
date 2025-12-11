# API Specification – Google Photos Lite: Memories for Families

**Version:** 1.0
**Owner:** Sujeeth Kumar Tuniki
**Last Updated:** December 11, 2025

---

# 1. Purpose

This document defines the **high-level API endpoints** that power Google Photos Lite.
It is written from a **Product Manager’s perspective**, focusing on:

* What each endpoint does
* Why it exists
* What inputs/outputs are expected
* How it enables user-facing functionality

This is not an engineering-level schema; it is a **product-facing API contract**.

---

# 2. API Overview

The system exposes a REST API with endpoints grouped into:

1. **Photo Ingestion & Retrieval**
2. **Search**
3. **Albums**
4. **Memories**
5. **Instagram Narrative Generation**

Each endpoint returns JSON.

---

# 3. Authentication (Future Scope)

V1 does **not** implement user authentication.
All endpoints assume a single-user system.
Future versions may add OAuth or Google Sign-In.

---

# 4. Endpoints

---

# 4.1 **POST /upload**

Uploads one or more photos and pushes them through the ingestion pipeline.

### **Purpose**

* Allow users to upload media
* Trigger Google Vision AI labeling
* Generate thumbnails
* Save metadata

### **Request**

```
multipart/form-data
{
  files: [binary images]
}
```

### **Response**

```json
{
  "uploaded_count": 12,
  "photo_ids": ["p1", "p2", ...]
}
```

### **Errors**

* 400: No file provided
* 413: File too large
* 500: Ingestion pipeline error

---

# 4.2 **GET /photos**

Fetches paginated list of photos for the grid view.

### **Purpose**

* Display user's library
* Allow infinite scrolling

### **Query Params**

| Param | Type | Description                  |
| ----- | ---- | ---------------------------- |
| page  | int  | Page number                  |
| limit | int  | Items per page (default: 30) |

### **Response**

```json
{
  "page": 1,
  "photos": [
    { "id": "p1", "thumbnail_url": "...", "timestamp": "2024-09-12T10:23Z" }
  ]
}
```

---

# 4.3 **GET /photos/{photo_id}**

Fetches full metadata for a single photo.

### **Purpose**

Support the Photo Detail View.

### **Response**

```json
{
  "id": "p1",
  "file_url": "...",
  "timestamp": "...",
  "labels": ["beach", "child", "smile"],
  "exif": {...},
  "embedding_cluster": "cluster_01",
  "thumbnail_url": "..."
}
```

---

# 4.4 **GET /search**

Keyword and semantic search.

### **Purpose**

Enable “Google-quality” search, e.g.

> "kid laughing on the beach"

### **Query Params**

| Param      | Type   | Description  |
| ---------- | ------ | ------------ |
| q          | string | Search query |
| start_date | string | Optional     |
| end_date   | string | Optional     |
| album_id   | string | Optional     |

### **Response**

```json
{
  "query": "kid beach",
  "results": [
    { "id": "p12", "thumbnail_url": "...", "score": 0.92 }
  ]
}
```

---

# 4.5 **POST /narrative**

Generates an Instagram-ready narrative from selected photos.

### **Purpose**

Convert AI insights → storytelling caption.

### **Request**

```json
{
  "photo_ids": ["p1", "p2"],
  "tone": "emotional",
  "user_prompt": "My son's first beach trip"
}
```

### **Response**

```json
{
  "narrative": "A tiny explorer meets the endless ocean...",
  "caption": "Tiny feet. Big waves. Bigger memories.",
  "hashtags": ["#familymoments", "#beachday", "#memories"]
}
```

---

# 4.6 **GET /memories**

Retrieves pre-generated or on-demand memories.

### **Purpose**

Display memory cards inside UI.

### **Response**

```json
{
  "memories": [
    {
      "id": "m1",
      "title": "Last Month Highlights",
      "cover_photo": "p33",
      "photo_count": 12
    }
  ]
}
```

---

# 4.7 **GET /memories/{memory_id}**

Returns full set of photos in a memory for slideshow.

```json
{
  "id": "m1",
  "title": "Last Month Highlights",
  "photos": ["p10", "p11", ...]
}
```

---

# 4.8 **POST /albums**

Creates a new manual album.

### **Request**

```json
{
  "name": "Family Trip"
}
```

### **Response**

```json
{
  "album_id": "a1",
  "name": "Family Trip"
}
```

---

# 4.9 **GET /albums**

Lists all albums.

```json
{
  "albums": [
    { "id": "a1", "name": "Family Trip", "photo_count": 42 }
  ]
}
```

---

# 4.10 **POST /albums/{album_id}/add**

Adds photos to album.

### **Request**

```json
{
  "photo_ids": ["p1", "p2"]
}
```

### **Response**

```json
{
  "album_id": "a1",
  "added": 2
}
```

---

# 4.11 **POST /albums/{album_id}/remove**

```json
{
  "photo_ids": ["p1"]
}
```

---

# 5. Error Handling (Product Rules)

### The system must:

* Return clear human-readable messages
* Not expose internal stack traces
* Handle Google Vision AI failures gracefully
* Never silently drop photos

**Examples:**

* “Unable to generate narrative. Please try again.”
* “One or more photos failed to upload.”

---

# 6. Versioning

All APIs live under:

```
/api/v1/
```

This allows future non-breaking upgrades.

---

# 7. Summary

This API spec reflects an **end-to-end product understanding** of how a modern photo system works:

* Upload
* AI labeling
* Retrieval
* Search
* Memories
* Albums
* Narrative generation

Together, these APIs power a meaningful subset of Google Photos capabilities.
