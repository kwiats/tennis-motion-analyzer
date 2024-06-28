import os
import base64
import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse

from src.config import UPLOAD_DIR, PROCESSED_DIR
from src.ml.estimators.media_pipe_estimator import MediaPipePoseEstimator

router = APIRouter()


def process_frame(frame):
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return processed_frame


@router.get("/camera_feed")
async def camera_feed():
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    processed_frame = process_frame(frame)
    _, jpeg = cv2.imencode(".jpg", processed_frame)
    return JSONResponse({"image": jpeg.tobytes().hex()})


@router.post("/process_image")
async def process_image(request: Request):
    data = await request.json()
    image_data = data["image"].split(",")[1]
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, jpeg = cv2.imencode(".jpg", processed_img)
    jpeg_base64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return JSONResponse({"image": jpeg_base64})


@router.post("/upload_video")
async def upload_video(video: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    input_path = os.path.join(UPLOAD_DIR, video.filename)
    output_path = os.path.join(
        PROCESSED_DIR, "processed_" + os.path.splitext(video.filename)[0] + ".mp4"
    )

    with open(input_path, "wb+") as f:
        f.write(await video.read())

    estimator = MediaPipePoseEstimator()
    estimator.process_video(input_path, output_path)

    if not os.path.exists(output_path):
        return JSONResponse({"error": "Processed video not found"}, status=500)

    return JSONResponse({"output_path": output_path})


@router.get("/{file_path:path}")
async def download_video(file_path: str):
    if os.path.exists(file_path):
        return FileResponse(
            file_path, media_type="video/mp4", filename=os.path.basename(file_path)
        )
    else:
        return JSONResponse({"error": "File not found"}, status=404)
