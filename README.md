# 📸 Google Photos Lite — Intelligent Photo Curation (V1)

## Why this project exists

**Google Photos Lite (V1)** is a prototype that shows how AI can **remove the manual effort of selecting photos and writing captions** for sharing.

Modern photo apps store thousands of photos, but sharing a great moment still requires manual effort:

* Selecting the best photos
* Filtering by date or theme
* Writing a narrative/caption (e.g. Instagram)

To reduce the hassle:

* The app connects directly to a **local photo folder**
* Lets users **search by intent + date**
* **Ranks the best photos automatically**
* Generates an **Instagram-ready narrative**

**Key insight:**
The value is not storing photos — it’s **Search → Rank → Narrative** as a single flow.

➡️ Repo shows how this can evolve into a Google Photos / Apple Photos–grade feature. This project explores **how AI-assisted curation can reduce that friction**, starting with a pragmatic, explainable V1.

---

## What this app does (V1)

**Photos Lite (V1)** connects to a **local photo folder** and provides:

### ✅ 1. Intelligent Photo Discovery

* Reads photos directly from a local folder (`~/Pictures/Mypicslite`)
* Extracts EXIF metadata (date, camera, resolution, orientation)
* No manual uploads required

### ✅ 2. Time-based Memories

Automatically creates memories like:

* Today
* This Week
* This Month

Each memory:

* Ranks photos by **quality score**
* Selects the **best cover photo**
* Limits output to top photos (req: user may take duplicates of the same picture and showing all such photos is unnecessary)

### ✅ 3. Search → Rank → Narrative Flow

Users can:

* Search photos using natural intent
  Examples:

  * `nature in November`
  * `baby photos in October`
* Filter by date range
* Get **top-ranked photos**, not raw dumps
* Receive an **Instagram-ready narrative**

### ✅ 4. Semantic Intent (V1 – heuristic)

Instead of raw filename matching, V1 supports **intent buckets**:

| Intent | Example Keywords             |
| ------ | ---------------------------- |
| nature | tree, forest, mountain, park |
| beach  | sea, ocean, sand, wave       |
| baby   | baby, kid, child             |
| food   | food, meal, lunch            |

> This logic is intentionally deterministic and explainable.
> In V2, this will be replaced with Vision or embedding-based understanding.

---

## Example User Flow (End-to-End)

**User prompt**

```
Give me Top 5 nature photos from November
```

**System output**

* Top 5 best photos (ranked by quality)
* Automatically selected cover image
* Narrative:

> *“Peaceful moments in nature from November, captured on my iPhone 14 Pro 🌿✨”*

The user can:

* Post photos directly to Instagram
* Copy-paste the narrative
* Avoid manual curation entirely

---

## How ranking works (V1 – explainable by design)

Each photo receives a **quality score** based on:

* Resolution (higher = better)
* Recency (newer preferred)
* Orientation penalty (rotated / odd orientation)

This keeps the system:

* Deterministic
* Debuggable

---

## Architecture Overview

```
Routes (API)
 ├── /photos        → List local photos
 ├── /memories      → Time-based memories
 ├── /search        → Search + rank
 └── /narrative     → Generate captions

Services (Business Logic)
 ├── local_photos_service.py
 ├── memories_service.py
 ├── search_service.py
 └── narrative_service.py
```

**Design principle**

* Routes handle HTTP concerns
* Services own domain logic

This separation enables clean evolution toward Google Photos API or Apple Photos API in V2.

---

## What’s intentionally NOT in V1

This is a **product decision**, not a limitation.

* ❌ Vision APIs (Google Vision, Apple Vision)
* ❌ Face recognition
* ❌ Deep ML tagging

**Why?**
V1 validates whether **Search → Rank → Narrative** meaningfully improves user experience before adding ML complexity.

---

## Planned V2 Enhancements

* Google Photos / Apple Photos API integration
* Vision-based tagging (objects, scenes, faces)
* Embedding-based semantic search
* Personal style-based narratives
* Multi-album sharing workflows

---

## Why this project matters

This project demonstrates:

* Product thinking before ML complexity
* Clear V1 → V2 evolution
* AI used as **UX leverage**, not hype
* Ability to ship, test, and iterate

---

## Tech Stack

* Python
* FastAPI
* EXIF parsing
* Local filesystem ingestion
* Deterministic ranking logic

---

## Demo

*(Screenshots to be added)*

---

## Author

**Sujeeth Kumar Tuniki**
Senior Product Manager @ Amazon
Sydney, Australia