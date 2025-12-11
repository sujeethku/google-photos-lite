# Product Requirements – Google Photos Lite: Memories for Families

**Version:** 1.0
**Owner:** Sujeeth Kumar Tuniki
**Last Updated:** December 11, 2025

---

# 1. Purpose of This Document

This document outlines the **user-facing product requirements** for Google Photos Lite.
It focuses on *what* the system must do to deliver user value, not *how* it should be implemented.

These requirements cover V1, reflecting:

* Core photo management
* AI-assisted search and organization
* Memory generation
* Instagram-ready narrative generation

---

# 2. Guiding Product Principles

1. **Zero-effort Organization**
   Users should not need to manually tag or sort photos.

2. **AI as a Memory Engine**
   AI identifies meaningful moments and themes automatically.

3. **Search Should Feel Magical**
   Descriptions like “my son laughing on the beach” should return results.

4. **Storytelling is Part of Memory Creation**
   Users should instantly get shareable narratives from selected images.

5. **Simple, Calm UI**
   Avoid complexity; the value is in the intelligence, not the interface.

---

# 3. Functional Requirements

## 3.1 Photo Upload & Ingestion

### User Requirements

* Users must be able to upload **single or multiple** photos at once.
* Uploading must show a clear **progress indicator**.
* After upload, photos should appear almost immediately in the grid view.
* Users should not need technical knowledge (e.g., EXIF) to use the app.

### System Requirements

* System must extract metadata automatically:

  * Timestamp
  * EXIF (device, aperture, GPS when available)
* System must generate a thumbnail for fast preview.
* System must create a database entry with:

  * File URLs
  * Labels
  * Embeddings
  * EXIF
  * Timestamps

---

## 3.2 Photo Library (Grid View)

### User Requirements

* Users must be able to scroll through their entire collection.
* Photos must load in chronological order (newest → oldest).
* Grid must support:

  * Infinite scroll
  * Responsive design (desktop + mobile)
* Clicking a photo opens detail view.

### System Requirements

* Grid must retrieve paginated photo data.
* Grid should load additional photos automatically when user scrolls near the end.

---

## 3.3 Photo Detail View

### User Requirements

* Users must be able to see:

  * Large preview of the image
  * Metadata (timestamp, EXIF summary)
  * AI-generated labels
* User must be able to:

  * Add to album
  * Generate an Instagram narrative

### System Requirements

* Must fetch:

  * Image URL
  * All stored metadata
  * AI labels
  * Embedding cluster info

---

## 3.4 AI Labeling (Powered by Google Vision AI)

### User Requirements

* No user action should be needed to categorize photos.
* Labels must be accurate enough to aid search & memories.

### System Requirements

* System must automatically call **Google Vision AI** for:

  * Object detection
  * Scene classification
  * Emotion inference (if available)
  * Color analysis
  * Embedding generation (vector)

* Must store:

  * List of labels
  * Confidence scores
  * Embeddings

---

## 3.5 Search

### User Requirements

* Users must be able to search using natural descriptions (e.g., “kids playing in water”).
* Users must be able to filter by:

  * Date range
  * Album

### System Requirements

* Search must support:

  * Keyword-based search (using labels & metadata)
  * Semantic search (using embeddings)
  * Results must appear < 1 second for typical dataset (~1k photos).

---

## 3.6 Albums

### User Requirements

Users must be able to:

* Create a new album
* Add photos to albums
* Remove photos from albums
* View album contents

The system may also suggest albums (optional in V1):

* Kids
* Beaches
* Smiles
* Food

### System Requirements

* Each album has a name + timestamp.
* Photos in albums must appear in the same grid style as the library.

---

## 3.7 Memories (Time-Based & Theme-Based)

### User Requirements

Users must be able to view:

* “Week in Review”
* “Last Month Highlights”
* “One Year Ago Today”
* Theme Memories:

  * Kids
  * Beach
  * Birthday
  * Pets

Memories must:

* Look visually appealing (cover image + title + count)
* Play as a slideshow when opened

### System Requirements

* Photos must be clustered by:

  * Time
  * Theme (based on labels from Google Vision AI)

* Quality scoring must pick the best images:

  * Sharpness
  * Brightness
  * Face presence
  * Variety

---

## 3.8 Instagram Narrative Generator (Key Differentiator)

### User Requirements

When selecting 1–10 photos, users must be able to:

* Click **“Generate Narrative”**
* Receive:

  * A storytelling paragraph
  * An Instagram-ready caption
  * Hashtag suggestions
* Choose tone:

  * Emotional
  * Fun
  * Minimalistic
  * Inspirational

### System Requirements

* Inputs to narrative generator:

  * Google Vision AI labels
  * Objects detected
  * Emotions (if available)
  * EXIF hints (location, time of day)
  * Optional user prompt

* Output must be:

  * Cohesive
  * Emotionally grounded
  * Grammatically correct
  * Ready for copy-paste into Instagram

---

# 4. Non-Functional Requirements

## 4.1 Performance

* Search must return results in <300ms (backend processing).
* Memory generation must complete in <2 seconds for 100 photos.
* Upload pipeline should process a photo in <1 second on average (excluding external API latency).

## 4.2 Scalability

* Must support at least 1,000 photos per user without degradation.
* Vector search must scale horizontally.

## 4.3 Reliability

* Upload failures must show clear error messaging.
* System must retry AI labeling if Google Vision AI fails.

## 4.4 Usability

* UI must be simple, clean, and styled to resemble Google Photos culture.
* No user should need technical knowledge to operate the system.

## 4.5 Security

* Uploaded files must not be publicly accessible without signed URLs.
* AI interactions must not expose API keys.

---

# 5. Success Metrics

### Primary

* % of photos successfully labeled
* Search success rate
* Memory engagement rate
* Narrative generation usage

### Secondary

* Albums created
* Daily active sessions
* Repeat visits

---

# 6. Out of Scope for V1

* Collaborative albums
* Advanced editing (Magic Eraser, etc.)
* Full mobile app
* Social sharing inside the app
* Offline mode

---

# 7. Summary

This requirements document describes the **user-facing, product-level behaviors** needed to power Google Photos Lite: a polished, AI-driven photo management experience with modern features such as semantic search, memory creation, and narrative generation.