from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import video

app = FastAPI(
    version="0.1",
    title="Pose Estimation API",
    description="API for pose estimation using MediaPipe and YOLO",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/video", tags=["video"])
