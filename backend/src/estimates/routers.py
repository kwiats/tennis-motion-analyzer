from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.estimates.repository import EstimatesRepository
from src.estimates.schemas import EstimateCreate, Estimate, EstimateUpdate
from src.estimates.services import EstimatesService
from src.ml.estimators.media_pipe_estimator import MediaPipePoseEstimator
from src.sql.database import get_db

estimator_router = APIRouter()

estimator_repository = EstimatesRepository()
estimator = MediaPipePoseEstimator()

estimator_service = EstimatesService(estimator_repository, estimator)


@estimator_router.post("/predict", response_model=Estimate)
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    empty_estimate = EstimateCreate(
        sex="", age=0, height=0.0, weight=0.0, activity_level="", impact_type=""
    )
    return await estimator_service.predict(empty_estimate, file, db)


@estimator_router.put("/predict/{estimate_id}", response_model=Estimate)
async def update_estimate(
    estimate_id: int,
    sex: str = Form(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    activity_level: str = Form(...),
    impact_type: str = Form(...),
    db: Session = Depends(get_db),
):
    update_data = EstimateUpdate(
        sex=sex,
        age=age,
        height=height,
        weight=weight,
        activity_level=activity_level,
        impact_type=impact_type,
    )
    return estimator_service.update_estimate(estimate_id, update_data, db)
