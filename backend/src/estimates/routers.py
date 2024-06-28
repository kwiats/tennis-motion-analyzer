from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.estimates.repository import EstimatesRepository
from src.estimates.schemas import EstimateCreate, Estimate
from src.estimates.services import EstimatesService
from src.ml.estimators.media_pipe_estimator import MediaPipePoseEstimator
from src.sql.database import get_db

estimator_router = APIRouter()

estimator_repository = EstimatesRepository()
estimator = MediaPipePoseEstimator()

estimator_service = EstimatesService(estimator_repository, estimator)


@estimator_router.post("/predict", response_model=Estimate)
async def predict_estimate(
    sex: str = Form(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    activity_level: str = Form(...),
    impact_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    estimate = EstimateCreate(
        sex=sex,
        age=age,
        height=height,
        weight=weight,
        activity_level=activity_level,
        impact_type=impact_type,
    )
    return await estimator_service.add_estimate(estimate, file, db)
