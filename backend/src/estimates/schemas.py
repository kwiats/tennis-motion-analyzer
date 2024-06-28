from pydantic import BaseModel


class EstimateBase(BaseModel):
    sex: str
    age: int
    height: float
    weight: float
    activity_level: str
    impact_type: str


class EstimateCreate(EstimateBase):
    pass


class Estimate(EstimateBase):
    id: int
    input_path: str
    output_path: str

    class Config:
        orm_mode: bool = True
