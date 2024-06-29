import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from src.sql.database import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    bucket_name: Mapped[str] = Column(String, index=True)
    file_name: Mapped[str] = Column(String)
    file_type: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
