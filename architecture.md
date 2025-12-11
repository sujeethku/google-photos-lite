# Architecture – [Mock App] Google Photos Lite: Memories for Families

**Version:** 1.0
**Owner:** Sujeeth Kumar Tuniki
**Last Updated:** December 11, 2025

---

# 1. High-Level Architecture Overview

This application follows a modular, scalable architecture designed to mimic the core data and AI pipeline of Google Photos:

```
                     ┌───────────────────────────┐
                     │         Frontend          │
                     │     (React + Tailwind)    │
                     │ ───────────────────────── │
                     │  • Photo Grid             │
                     │  • Upload UI              │
                     │  • Search Bar             │
                     │  • Albums                 │
                     │  • Memories Viewer        │
                     └──────────────┬────────────┘
                                    │  REST API Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend API (FastAPI)                   │
│ ─────────────────────────────────────────────────────────────── │
│  Endpoints:                                                     │
│    POST /upload            → Ingestion Pipeline                 │
│    GET /photos             → Fetch paginated library            │
│    GET /photos/{id}        → Photo detail                       │
│    GET /search             → Keyword + semantic search          │
│    GET /memories           → Fetch generated memories           │
│    POST /albums            → Create album                       │
│    GET /albums             → View albums                        │
│                                                                 │
│  Backend Internal Modules:                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Ingestion Service                                          | │
│  │  • Save raw file to storage                                | │
│  │  • Generate thumbnail                                      | │
│  │  • Extract EXIF metadata                                   | │
│  │  • Call AI Vision Model (labels + embeddings)              | │
│  │  • Store record in DB                                      | │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Search Engine                                              | │
│  │  • Keyword search (labels, metadata)                       | │
│  │  • Vector similarity search (pgvector / FAISS)             | │
│  │  • Combined scoring                                        | │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Memory Engine                                              │ |
│  │  • Time clustering (days/weeks)                            │ |
│  │  • Theme clustering (label density: beach, kids, smiles)   │ |
│  │  • Quality scoring (sharpness, brightness, faces)          │ |
│  │  • Select top photos for each memory                       │ |
│  │  • Cache final memory cards in DB                          │ |
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
      ┌────────────────────────────────────────────────────┐
      │                Data Layer (Storage + DB)           │
      │ ────────────────────────────────────────────────── │
      │                                                    │
      │  📦 Object Storage (S3 or GCS)                     | 
      │    • Original photos                               │
      │    • Thumbnails                                    │
      │                                                    │
      │  🗄️ Database (PostgreSQL + pgvector)               │
      │    Tables:                                         │
      │      photos                                        │
      │        - id                                        │
      │        - file_url                                  │
      │        - thumb_url                                 │
      │        - timestamp                                 │
      │        - labels (json)                             │
      │        - embedding (vector)                        │
      │        - exif (json)                               │
      │      albums                                        │
      │      memories                                      │
      └────────────────────────────────────────────────────┘
                               │
                               ▼
                 ┌──────────────────────────────────┐
                 │      AI/Vision Model Layer       │
                 │ ──────────────────────────────── │
                 │  • Gemini Vision API (labeling)  │
                 │  • OR OpenAI Vision              │
                 │  • OR CLIP for open-source       │
                 │                                  │
                 │ Outputs:                         │
                 │  - Scene labels                  │
                 │  - Object tags                   │
                 │  - Embedding vector              │
                 │  - Faces/people detection        │
                 └──────────────────────────────────┘
```

---

# 2. Architectural Principles

### **2.1 Separation of Concerns**

Each layer is independent:

* Frontend handles presentation
* Backend handles ingestion, search, and memories
* AI layer handles photo intelligence
* Storage + DB handle persistence

### **2.2 Scalability**

* Object storage decouples file management
* Vector database scales semantic search
* FastAPI supports async workloads
* Architecture supports horizontal scaling

### **2.3 Extensibility**

Future enhancements (face clustering, trip detection, video highlights) require no redesign — only module expansion.

---

# 3. Component Breakdown

## **3.1 Frontend (React + Tailwind)**

Responsibilities:

* Photo upload UI
* Infinite scroll grid
* Photo detail model
* Album pages
* Memories view
* Search filtering
* Narrative generation UI

---

## **3.2 Backend API (FastAPI)**

### Key Responsibilities:

* Receives uploads
* Generates thumbnails
* Extracts metadata
* Calls AI vision models
* Stores metadata + vectors
* Performs keyword + semantic search
* Generates memories
* Generates Instagram narratives

### API Endpoints:

| Method | Endpoint     | Description                     |
| ------ | ------------ | ------------------------------- |
| POST   | /upload      | Upload images → ingest pipeline |
| GET    | /photos      | List photos                     |
| GET    | /photos/{id} | Full metadata + labels          |
| GET    | /search      | Search grid results             |
| POST   | /narrative   | Generate Instagram caption      |
| GET    | /memories    | Fetch generated memories        |
| POST   | /albums      | Create album                    |
| GET    | /albums      | List albums                     |

---

# 4. Ingestion Pipeline

Steps when a new photo is uploaded:

1. **Receive image**
2. **Store raw file in S3/GCS**
3. **Generate thumbnail (Pillow)**
4. **Extract EXIF metadata**
5. **Call AI Vision model**

   * Labels
   * Embedding
   * Scene info
6. **Store DB record**
7. **Write logs for debugging**

This mimics real Google Photos ingestion flow in simplified form.

---

# 5. AI Layer

### **Models Supported**

* **Gemini Vision API**

### **Outputs stored:**

* Labels (JSON)
* Embedding vector
* Color palette
* Emotion indicators
* Objects detected

---

# 6. Search Architecture

### **Keyword Search**

Matches:

* Labels
* EXIF metadata
* Album names

### **Semantic Search (Vector Search)**

Uses:

* **pgvector** extension in PostgreSQL
  or
* **FAISS** (local vector store)

User enters:

> “my kid laughing on the beach”

System:

* Converts query → embedding
* Finds nearest vectors
* Ranks results

---

# 7. Memories Engine

### Inputs:

* All stored labels
* Embeddings
* Timestamps

### Processing:

* Time clustering
* Label clustering
* Quality scoring
* Selecting top photos

### Output:

* “Week in Review”
* “Birthday Memories”
* “Family Trip”

---

# 8. Instagram Narrative Engine

### Inputs:

* Selected photos
* Labels
* EXIF
* Optional user context

### Output:

* Narrative paragraph
* Instagram caption
* Hashtag suggestions

---

# 9. Data Model Summary

### **photos table**

* id
* file_url
* thumbnail_url
* timestamp
* labels (json)
* embedding (vector)
* exif (json)

### **albums table**

* id
* name
* created_at

### **album_photos**

* album_id
* photo_id

### **memories**

* id
* title
* photo_ids[]

---

# 10. Diagram Notes for GitHub Reviewers

* Architecture is modular and production-inspired
* Mirrors real Google Photos components
* Demonstrates understanding of ingestion → AI → search → UX flow
* Clear reasoning for each design choice
* Easy to extend to V2/V3 features
