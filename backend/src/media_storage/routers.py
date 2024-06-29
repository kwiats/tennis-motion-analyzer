import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Response, UploadFile
from sqlalchemy.orm import Session

from src.core.minio_cloud_storage import MinioCloudStorage
from src.media_storage.repository import MediaRepository
from src.media_storage.schemas import MediaFile, MediaRead, MediaUpdate, MediaCreate
from src.media_storage.services import MediaService
from src.sql.database import get_db

media_router = APIRouter()

media_repository = MediaRepository()
cloud_storage = MinioCloudStorage()
media_service = MediaService(repository=media_repository, storage=cloud_storage)


@media_router.post("/upload")
def create_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Response:
    media_create = MediaCreate(
        file_name=file.filename,
        file_type=file.content_type,
    )
    return media_service.create_media(db, media_create, file)


@media_router.get("/{media_id}")
def get_media(
    media_id: str,
    db: Session = Depends(get_db),
) -> List[MediaRead]:
    return media_service.get_media_obj(media_id, db)


@media_router.patch("/{media_id}/update")
def update_media(
    media_id: str,
    media_update: MediaUpdate,
    db: Session = Depends(get_db),
) -> MediaRead:
    return media_service.update_media(db, media_id, media_update)


@media_router.delete("/{media_id}/delete")
def delete_media(
    media_id: str,
    db: Session = Depends(get_db),
) -> Response:
    return media_service.delete_media(db, media_id)


@media_router.get("/{bucket_name}/{object_id}/{filename}")
def open_media_from_cloud_storage(
    bucket_name: str,
    object_id: int | str | uuid.UUID,
    filename: str,
):
    return media_service.get_media_file(
        MediaFile(
            bucket_name=bucket_name,
            file_name=filename,
            id_object=object_id,
        )
    )


@media_router.get("/{bucket_name}/{filename}")
def open_default_media_from_cloud_storage(bucket_name: str, filename: str):
    return media_service.get_media_file(
        MediaFile(bucket_name=bucket_name, file_name=filename)
    )
