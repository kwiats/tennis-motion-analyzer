import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from sqlalchemy.orm import Session

from src.media_storage.models import Media
from src.media_storage.schemas import MediaCreate, MediaUpdate


class IRepository(ABC):
    @abstractmethod
    def get_by_attraction_id(
        self, db: Session, attraction_id: int
    ) -> Optional[List[Media]]:
        pass

    @abstractmethod
    def get_by_comment_id(
        self, db: Session, comment_id: Union[str, uuid.UUID]
    ) -> Optional[List[Media]]:
        pass

    @abstractmethod
    def get_by_review_id(
        self, db: Session, review_id: Union[str, uuid.UUID]
    ) -> Optional[List[Media]]:
        pass

    @abstractmethod
    def get_by_id(self, db: Session, file_id: str) -> Optional[Media]:
        pass

    @abstractmethod
    def create(self, db: Session, media: MediaCreate) -> bool:
        pass

    @abstractmethod
    def update(
        self, db: Session, existing_media: Media, media: MediaUpdate
    ) -> Optional[Media]:
        pass

    @abstractmethod
    def delete(self, db: Session, media: Media) -> bool:
        pass
