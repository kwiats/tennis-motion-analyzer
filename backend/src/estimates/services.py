import os

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from src.config import UPLOAD_DIR, PROCESSED_DIR


class EstimatesService:
    def __init__(self, estimates_repository, estimator):
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

    async def add_estimate(self, estimates, file: UploadFile, db: Session):
        try:
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            os.makedirs(PROCESSED_DIR, exist_ok=True)

            input_path = os.path.join(UPLOAD_DIR, file.filename)
            output_path = os.path.join(
                PROCESSED_DIR,
                "processed_" + os.path.splitext(file.filename)[0] + ".mp4",
            )
            file_content = await file.read()

            with open(input_path, "wb+") as f:
                f.write(file_content)

            self.estimator.process_video(input_path, output_path)

            return self.estimates_repository.add_estimate(estimates, db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    def delete_estimate(self, estimate_id, db: Session):
        try:
            return self.estimates_repository.delete_estimate(estimate_id, db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
