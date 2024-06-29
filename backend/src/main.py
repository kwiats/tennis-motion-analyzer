from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.estimates.routers import estimator_router
from src.media_storage.routers import media_router

tags_metadata = [
    {
        "name": "estimates",
        "description": "Manage estimate predictions and related data.",
    },
    {
        "name": "media",
        "description": "Manage media stored in cloud services and related data.",
    },
]

app = FastAPI(
    root_path="/api",
    version="0.1",
    title="Tennis Motion Analyzer API",
    description="API for pose estimation using MediaPipe and YOLO",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(estimator_router, prefix="/estimates", tags=["estimates"])
app.include_router(media_router, prefix="/media", tags=["media"])
