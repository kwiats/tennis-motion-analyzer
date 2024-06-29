from abc import ABC, abstractmethod
from typing import BinaryIO, List, Union

from minio.datatypes import Bucket, Object


class ICloudStorage(ABC):
    @abstractmethod
    def create_bucket(self, bucket_name: str) -> None:
        pass

    @abstractmethod
    def check_bucket(self, bucket_name: str) -> bool:
        pass

    @abstractmethod
    def list_buckets(self) -> Union[List[Bucket], str]:
        pass

    @abstractmethod
    def list_bucket_objects(
        self, bucket_name: str, prefix: str | None = None, recursive: bool = False
    ) -> List[Object]:
        pass

    @abstractmethod
    def upload_file(
        self,
        bucket_name: str,
        filename: str,
        file: BinaryIO,
        file_size: int,
        content_type: str | None = None,
    ) -> None:
        pass

    @abstractmethod
    def retrieve_file(self, bucket_name: str, filename: str) -> bytes:
        pass
