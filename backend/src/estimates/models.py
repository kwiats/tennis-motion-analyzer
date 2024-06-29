import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, UUID
from sqlalchemy.orm import Mapped

from src.sql.database import Base


class Estimate(Base):
    __tablename__ = "estimates"

    id: Mapped[uuid.UUID] = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    sex: Mapped[str] = Column(String, index=True)
    age: Mapped[int] = Column(Integer)
    height: Mapped[float] = Column(Float)
    weight: Mapped[float] = Column(Float)
    activity_level: Mapped[str] = Column(String)
    impact_type: Mapped[str] = Column(String)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
