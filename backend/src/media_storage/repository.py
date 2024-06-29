import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from src.media_storage.models import Media
from src.media_storage.repository_interface import IRepository
from src.media_storage.schemas import MediaCreate, MediaUpdate

logger = logging.getLogger(__name__)


class MediaRepository(IRepository):
    def get_by_attraction_id(self, db: Session, attraction_id: int) -> List[Media]:
        return db.query(Media).filter(Media.attraction_id == attraction_id).all()

    def get_by_comment_id(self, db: Session, comment_id: str) -> List[Media]:
        return db.query(Media).filter(Media.comment_id == comment_id).all()

    def get_by_review_id(self, db: Session, review_id: str) -> List[Media]:
        return db.query(Media).filter(Media.review_id == review_id).all()

    def get_by_id(self, db: Session, file_id: str) -> Optional[Media]:
        return db.query(Media).filter(Media.id == file_id).first()

    def create(self, db: Session, media_data: MediaCreate) -> bool:
        try:
            with db.begin():
                new_media = Media(
                    bucket_name=media_data.bucket_name,
                    file_name=media_data.file_name,
                    file_type=media_data.file_type,
                    attraction_id=media_data.attraction_id,
                    comment_id=media_data.comment_id,
                    review_id=media_data.review_id,
                )
                db.add(new_media)

            return True
        except Exception as e:
            logger.error("Error: %s" % e)
            return False

    def update(
        self, db: Session, existing_media: Media, media: MediaUpdate
    ) -> Optional[Media]:
        try:
            with db.begin_nested():
                update_data = media.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(existing_media, key, value)
                db.add(existing_media)
                db.commit()
            return existing_media
        except Exception as e:
            logger.error("Error during update: %s" % e)
            return None

    def delete(self, db: Session, media: Media) -> bool:
        try:
            with db.begin_nested():
                db.delete(media)
                db.commit()
            return True
        except Exception as e:
            logger.error("Error during delete: %s" % e)
            return False
