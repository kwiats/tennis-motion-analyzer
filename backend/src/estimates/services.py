import os

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from src.config import settings
from src.estimates.schemas import Estimate, EstimateUpdate
from src.ml.estimators.pose_estimator_interface import PoseEstimatorInterface


class EstimatesService:
    def __init__(self, estimates_repository, estimator: PoseEstimatorInterface):
        self.estimates_repository = estimates_repository
        self.estimator = estimator

    def get_estimates(self, db: Session):
        try:
            return self.estimates_repository.get_estimates(db)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while fetching estimates: {str(e)}",
            )

    async def predict(self, estimates, file: UploadFile, db: Session) -> Estimate:
        try:
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            os.makedirs(settings.PROCESSED_DIR, exist_ok=True)

            input_path = os.path.join(settings.UPLOAD_DIR, file.filename)
            output_path = os.path.join(
                settings.PROCESSED_DIR,
                "processed_" + os.path.splitext(file.filename)[0] + ".mp4",
            )
            file_content = await file.read()

            with open(input_path, "wb+") as f:
                f.write(file_content)

            self.estimator.process_video(input_path, output_path)
            result = estimates
            # result = self.estimates_repository.add_estimate(estimates, db)
            return Estimate(
                id=0,
                age=result.age,
                gender=result.gender,
                height=result.height,
                weight=result.weight,
                activity_level=result.activity_level,
                impact_type=result.impact_type,
                input_path=input_path,
                output_path=output_path,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def update_estimate(
        self, estimate_id: int, update_data: EstimateUpdate, db: Session
    ):
        try:
            # estimate = self.estimates_repository.get_estimate_by_id(estimate_id, db)
            # if not estimate:
            #     raise HTTPException(status_code=404, detail="Estimate not found")

            # result = self.estimates_repository.update_estimate(estimate, update_data, db)
            result = update_data

            return Estimate(
                id=estimate_id,
                age=result.age,
                gender=result.gender,
                height=result.height,
                weight=result.weight,
                activity_level=result.activity_level,
                impact_type=result.impact_type,
                input_path="result.input_path",
                output_path="result.output_path",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while updating the estimate: {str(e)}",
            )

    def delete_estimate(self, estimate_id, db: Session):
        try:
            return self.estimates_repository.delete_estimate(estimate_id, db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
