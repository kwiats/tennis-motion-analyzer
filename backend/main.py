from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/video", tags=["video"])
