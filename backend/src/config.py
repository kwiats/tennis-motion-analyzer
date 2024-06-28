from pydantic.v1 import BaseSettings

YOLO_MODEL = "yolov5s"
UPLOAD_DIR = "static/uploads"
PROCESSED_DIR = "static/processed"


class GlobalConfig(BaseSettings):
    yolo_model: str = YOLO_MODEL
    upload_dir: str = UPLOAD_DIR
    processed_dir: str = PROCESSED_DIR


settings = GlobalConfig()
