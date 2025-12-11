# Folder Structure – Google Photos Lite: Memories for Families

**Version:** 1.0
**Owner:** Sujeeth Kumar Tuniki
**Last Updated:** December 11, 2025

This document describes the recommended folder structure for the V1 release of the Google Photos Lite app.

The structure is designed to be:

* Clean
* Modular
* Extensible
* Scalable

It reflects separation between:

* Frontend
* Backend
* Infrastructure
* Documentation

---

# 1. High-Level Structure

```
google-photos-lite/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies/
│   │   ├── core/
│   │   ├── services/
│   │   ├── models/
│   │   ├── db/
│   │   ├── utils/
│   │   ├── tests/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PhotoGrid/
│   │   │   ├── PhotoDetail/
│   │   │   ├── Upload/
│   │   │   ├── Albums/
│   │   │   ├── Memories/
│   │   │   └── Narrative/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/     # API calls
│   │   ├── assets/
│   │   └── App.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── docs/
│   ├── product_brief.md
│   ├── architecture.md
│   ├── requirements.md
│   ├── api_spec.md
│   ├── schema.md
│   └── folder_structure.md   # this file
│
├── .gitignore
└── README.md
```

---

# 2. Backend Structure Breakdown

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── photos.py
│   │   │   ├── search.py
│   │   │   ├── albums.py
│   │   │   ├── memories.py
│   │   │   └── narrative.py
│   │   └── dependencies/
│   │       └── vision_client.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py (future)
│   │
│   ├── services/
│   │   ├── ingestion_service.py
│   │   ├── search_service.py
│   │   ├── memory_service.py
│   │   └── narrative_service.py
│   │
│   ├── models/
│   │   ├── photo.py
│   │   ├── album.py
│   │   ├── memory.py
│   │   └── schemas.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   ├── migrations/
│   │   └── vector_ops.py
│   │
│   ├── utils/
│   │   ├── exif_reader.py
│   │   ├── thumbnailer.py
│   │   └── google_vision_mapper.py
│   │
│   ├── tests/
│   └── main.py
```

### Why this structure?

* **api/routes** → organizes endpoints cleanly
* **services/** → each business domain is isolated
* **models/** → defines DB models + Pydantic schemas
* **utils/** → general-purpose helpers
* **db/** → connection + migrations + vector functions

This reflects real-world microservice cleanliness.

---

# 3. Frontend Structure Breakdown

```
frontend/
├── src/
│   ├── components/
│   │   ├── PhotoGrid/
│   │   ├── PhotoDetail/
│   │   ├── Upload/
│   │   ├── Albums/
│   │   ├── Memories/
│   │   └── Narrative/
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Albums.jsx
│   │   ├── Memories.jsx
│   │   └── Narrative.jsx
│   │
│   ├── hooks/
│   ├── services/
│   │   ├── api.js
│   │   └── vision_mock.js (for dev)
│   │
│   ├── assets/
│   └── App.jsx
│
├── public/
└── package.json
```

### Why this structure?

* Aligns with React industry best practices
* Components are domain-separated
* Services folder centralizes all API calls

---

# 4. Docs Folder Structure

```
docs/
├── product_brief.md
├── architecture.md
├── requirements.md
├── api_spec.md
├── schema.md
└── folder_structure.md
```

Everything documentation-related lives in `docs/`, keeping repo root clean.

---

# 5. Future Enhancements (Folder-Level)

| Feature          | Folder Impact                            |
| ---------------- | ---------------------------------------- |
| Authentication   | backend/core, backend/api/routes/auth.py |
| Video processing | backend/services/video_service.py        |
| Face clustering  | backend/services/face_service.py         |
| Mobile app       | new folder: /mobile                      |
| Trip detection   | backend/services/trip_service.py         |
| Advanced editing | backend/services/editor_service.py       |

---

# 6. Summary

This folder structure:

* Demonstrates clean, scalable system organization
* Mirrors how real Google Photos or large-scale media apps are structured
* Prepares you to start implementing code with zero friction
