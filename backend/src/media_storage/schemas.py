import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MediaBase(BaseModel):
    id: Optional[uuid.UUID] = None
    bucket_name: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None


class MediaFile(BaseModel):
    file_name: str
    bucket_name: str
    id_object: int | str | uuid.UUID | None = None


class MediaCreate(MediaBase):
    pass


class MediaUpdate(MediaBase):
    updated_at: datetime = datetime.utcnow()


class MediaRead(MediaBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    bucket_name: str
    file_name: str
    file_type: str


class MediaReference(BaseModel):
    pass
