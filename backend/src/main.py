from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.endpoints import video
from src.estimates.routers import estimator_router

tags_metadata = [
    {
        "name": "video",
        "description": "Manage video-related options.",
    },
]

app = FastAPI(
    version="0.1",
    title="Pose Estimation API",
    description="API for pose estimation using MediaPipe and YOLO",
    openapi_tags=tags_metadata,
)

# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(video.router, prefix="/video", tags=["video"])
app.include_router(estimator_router, prefix="/estimates", tags=["estimates"])
