from fastapi import APIRouter, Depends, UploadFile, File
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
    return await estimator_service.predict(EstimateCreate(), file, db)


@estimator_router.put("/predict/{estimate_id}", response_model=Estimate)
async def update_estimate(
    estimate_id: int,
    estimate_data: EstimateUpdate,
    db: Session = Depends(get_db),
):
    return estimator_service.update_estimate(estimate_id, estimate_data, db)
