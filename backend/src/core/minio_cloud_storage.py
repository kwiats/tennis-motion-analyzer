import io
import logging
from mimetypes import guess_type
from typing import BinaryIO, Union

from fastapi import HTTPException
from minio import Minio, S3Error
from minio.datatypes import Bucket, Object

from src.config import settings
from src.core.interfaces.cloud_storage import ICloudStorage

logger = logging.getLogger(__name__)


class MinioCloudStorage(ICloudStorage):
    def __init__(
        self,
        api_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
        secure: bool | None = None,
    ):
        self.url = api_url or settings.MINIO_HOST_URL
        self.access_key = access_key or settings.MINIO_ACCESS_KEY
        self.secret_key = secret_key or settings.MINIO_SECRET_KEY
        self.secure: bool = secure or settings.MINIO_SECURE

        self.client = self._connect_to_cloudstorage()

    def _connect_to_cloudstorage(self) -> Minio:
        try:
            client = Minio(
                endpoint=self.url,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )
            self._check_connection(client)
            return client
        except Exception as e:
            logger.error("Failed to connect to MinIO server: %s" % e)
            raise HTTPException(
                status_code=500, detail="Unable to connect to MinIO server: %s" % e
            )

    def _check_connection(self, client: Minio):
        try:
            client.list_buckets()
        except S3Error as e:
            logger.error("MinIO S3 Error: %s" % e)
            raise HTTPException(status_code=500, detail="MinIO S3 Error: %s" % e)

        except Exception as e:
            logger.error("General error when checking connection to MinIO: %s" % e)
            raise HTTPException(
                status_code=500,
                detail="General error when checking connection to MinIO: %s" % e,
            )

    def create_bucket(self, bucket_name: str):
        try:
            if self.client.bucket_exists(bucket_name):
                raise HTTPException(
                    status_code=409, detail=f"Bucket '{bucket_name}' already exists."
                )
            self.client.make_bucket(bucket_name)
        except S3Error as e:
            logger.error("Error creating bucket '%s': %s" % (bucket_name, e))
            raise HTTPException(
                status_code=500, detail=f"Failed to create bucket '{bucket_name}': {e}"
            )

    def check_bucket(self, bucket_name: str) -> bool:
        return self.client.bucket_exists(bucket_name)

    def list_buckets(self) -> Union[list[Bucket], str]:
        try:
            return self.client.list_buckets()
        except S3Error as e:
            logging.error("Error listing buckets: %s " % e)
            raise HTTPException(status_code=500, detail=f"Failed to list buckets: {e}")

    def list_bucket_objects(
        self, bucket_name: str, prefix: str | None = None, recursive: bool = False
    ) -> list[Object]:
        try:
            return self.client.list_objects(
                bucket_name, prefix=prefix, recursive=recursive
            )
        except S3Error as e:
            logger.error("Error listing objects in bucket '%s': %s" % (bucket_name, e))
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list objects in bucket '{bucket_name}': {e}",
            )

    def upload_file(
        self,
        bucket_name: str,
        filename: str,
        file: BinaryIO,
        file_size: int,
        content_type: str | None = None,
    ):
        if not self.client.bucket_exists(bucket_name):
            raise HTTPException(
                status_code=404, detail=f"Bucket '{bucket_name}' does not exist."
            )

        content_type = (
            content_type or guess_type(filename)[0] or "application/octet-stream"
        )

        try:
            self.client.put_object(bucket_name, filename, file, file_size, content_type)
        except S3Error as e:
            logger.error(
                "Error uploading file '%s' to bucket '%s': %s"
                % (filename, bucket_name, e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file '{filename}' to bucket '{bucket_name}': {e}",
            )

    def retrieve_file(self, bucket_name: str, filename: str) -> bytes:
        if not self.client.bucket_exists(bucket_name):
            raise HTTPException(
                status_code=404, detail=f"Bucket '{bucket_name}' does not exist."
            )
        try:
            response = self.client.get_object(bucket_name, filename)
            with response:
                data_stream = io.BytesIO(response.data)
                data = data_stream.read()
            return data

        except S3Error as e:
            logger.error(
                "Error retrieving file '%s' from bucket '%s': %s"
                % (filename, bucket_name, e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve file '{filename}' from bucket '{bucket_name}': {e}",
            )
