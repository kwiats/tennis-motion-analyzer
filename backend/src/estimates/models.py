from src.sql.database import Base
from sqlalchemy import Column, Integer, String, Float


class Estimate(Base):
    __tablename__ = "estimates"

    id = Column(Integer, primary_key=True, index=True)
    sex = Column(String, index=True)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    activity_level = Column(String)
    impact_type = Column(String)
