from typing import Optional

from pydantic import BaseModel

from src.estimates.enums import Gender, ActivityLevel, ImpactType


class EstimateBase(BaseModel):
    gender: Optional[Gender] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    impact_type: Optional[ImpactType] = None


class EstimateCreate(EstimateBase):
    pass


class EstimateUpdate(EstimateBase):
    pass


class Estimate(EstimateBase):
    id: int
    input_path: str
    output_path: str

    class Config:
        from_attributes: bool = True
