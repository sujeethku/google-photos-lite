from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import photos, search, albums, memories, narrative
from app.api.routes import ingestion


app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registry
app.include_router(photos.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(albums.router, prefix="/api/v1")
app.include_router(memories.router, prefix="/api/v1")
app.include_router(narrative.router, prefix="/api/v1")
app.include_router(ingestion.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
