from pydantic.v1 import BaseSettings


class GlobalConfig(BaseSettings):
    YOLO_MODEL: str = "yolov5s"
    UPLOAD_DIR: str = "static/uploads"
    PROCESSED_DIR: str = "static/processed"
    MINIO_HOST_URL: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "aodlizJj8XGE9ieXzXIb"
    MINIO_SECRET_KEY: str = "114rXYV0a74wzHL5g8EX7C4VVS7mC2kyUC0HjyXF"
    MINIO_SECURE: bool = False

    class Config:
        env_file = ".env"


settings = GlobalConfig()
