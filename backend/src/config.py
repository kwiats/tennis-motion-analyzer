from pydantic.v1 import BaseSettings


class GlobalConfig(BaseSettings):
    YOLO_MODEL: str = "yolov5s"
    UPLOAD_DIR: str = "static/uploads"
    PROCESSED_DIR: str = "static/processed"

    class Config:
        env_file = ".env"


settings = GlobalConfig()
