# Database Schema – Google Photos Lite: Memories for Families

**Version:** 1.0
**Owner:** Sujeeth Tuniki
**Last Updated:** 2025
**AI Provider:** Google Vision AI (Gemini Vision API)

---

# 1. Purpose

This document defines the **database schema** for Google Photos Lite.

The design ensures:

* Fast retrieval of photos
* Efficient AI search (via vector embeddings)
* Support for albums and memories
* Compatibility with Google Vision AI outputs
* Scalability for future enhancements

The database used is **PostgreSQL** with the **pgvector** extension enabled.

---

# 2. Entity Relationship Diagram (Simplified)

```
 ┌──────────────┐          ┌────────────────┐
 │   photos     │          │    albums      │
 └───────┬──────┘          └──────┬─────────┘
         │                         │
         │  Many-to-Many          │
         ▼                         ▼
 ┌────────────────┐      ┌─────────────────────┐
 │  album_photos  │◄────►│      memories       │
 └────────────────┘      └─────────────────────┘
                   ▲               │
                   │               │ One-to-Many
                   └───────────────┘
```

---

# 3. Tables

---

# 3.1 **photos**

Stores all uploaded photos and AI-generated metadata.

| Column        | Type      | Description                                         |
| ------------- | --------- | --------------------------------------------------- |
| id            | UUID (PK) | Unique ID for the photo                             |
| file_url      | TEXT      | Location of original uploaded file                  |
| thumbnail_url | TEXT      | Location of thumbnail                               |
| timestamp     | TIMESTAMP | Extracted from EXIF or upload                       |
| exif          | JSONB     | Raw EXIF metadata                                   |
| labels        | JSONB     | Google Vision AI labels (objects, scenes, emotions) |
| embedding     | VECTOR    | pgvector embedding (used for semantic search)       |
| cluster_id    | TEXT      | Optional AI-generated cluster label                 |
| created_at    | TIMESTAMP | Upload time                                         |
| updated_at    | TIMESTAMP | Last update                                         |

### Notes

* Labels stored as arrays of `{label, confidence}`.
* Embeddings are 256–1024 dimensions (model-dependent).
* `cluster_id` enables grouping/photos for memories.

---

# 3.2 **albums**

Stores user-created albums.

| Column     | Type      | Description            |
| ---------- | --------- | ---------------------- |
| id         | UUID (PK) | Album ID               |
| name       | TEXT      | Album name             |
| created_at | TIMESTAMP | When album was created |

---

# 3.3 **album_photos** (Join Table)

Manages the many-to-many relationship between albums and photos.

| Column   | Type                  | Description              |
| -------- | --------------------- | ------------------------ |
| album_id | UUID (FK → albums.id) | Associated album         |
| photo_id | UUID (FK → photos.id) | Associated photo         |
| added_at | TIMESTAMP             | When the photo was added |

Primary Key: `(album_id, photo_id)`

---

# 3.4 **memories**

Stores metadata for memories (time-based or theme-based).

| Column      | Type                  | Description                             |
| ----------- | --------------------- | --------------------------------------- |
| id          | UUID (PK)             | Memory ID                               |
| title       | TEXT                  | Memory name                             |
| type        | TEXT                  | e.g., "week-in-review", "kids", "beach" |
| cover_photo | UUID (FK → photos.id) | Photo shown on memory card              |
| created_at  | TIMESTAMP             | Generated timestamp                     |

---

# 3.5 **memory_photos** (Join Table)

Stores the ordered set of photos in a memory slideshow.

| Column      | Type                    | Description           |
| ----------- | ----------------------- | --------------------- |
| memory_id   | UUID (FK → memories.id) | Memory                |
| photo_id    | UUID (FK → photos.id)   | Photo in the memory   |
| order_index | INT                     | Position in slideshow |

Primary Key: `(memory_id, photo_id)`

---

# 4. Index Strategy

### 4.1 Photos Table

* `CREATE INDEX idx_photos_timestamp ON photos(timestamp);`
* `CREATE INDEX idx_photos_labels ON photos USING GIN(labels);`
* `CREATE INDEX idx_photos_embedding ON photos USING ivfflat (embedding vector_cosine_ops);`

### Why?

* Fast chronological retrieval
* Fast label filtering
* Efficient vector search

---

# 5. Google Vision AI Mapping

Each Vision API response maps into structured columns:

### Example Response Fields → Schema Mapping

| Google Vision Output | Schema Column    |
| -------------------- | ---------------- |
| Objects Detected     | labels JSONB     |
| Scene Descriptions   | labels JSONB     |
| Dominant Colors      | labels JSONB     |
| Faces / Emotions     | labels JSONB     |
| Embedding vector     | embedding VECTOR |
| EXIF (if returned)   | exif JSONB       |

---

# 6. Future-Proofing

The schema is designed to easily support:

* Full face clustering
* Trip detection
* Video clip analysis
* User-specific personalization
* Shared albums (multi-user)
* Deleted photos bin
* Commenting / reactions

---

# 7. Summary

This schema:

* Mirrors the structural thinking behind Google Photos
* Prioritizes fast search, clean organization, and AI integration
* Supports all V1 requirements: albums, memories, narrative generation
* Demonstrates scalable, modern data design suitable for large systems
