from pydantic.v1 import BaseSettings


class GlobalConfig(BaseSettings):
    yolo_model: str = "yolov5s"
    upload_dir: str = "static/uploads"
    processed_dir: str = "static/processed"

    class Config:
        env_file = ".env"


settings = GlobalConfig()
