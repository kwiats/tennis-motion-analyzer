from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.estimates.models import Estimate
from src.estimates.schemas import EstimateUpdate


class EstimatesRepository:
    def get_estimates(self, db: Session) -> list[Estimate]:
        try:
            return db.query(Estimate).all()
        except Exception:
            raise

    def get_estimate_by_id(self, estimate_id: int, db: Session) -> Estimate:
        try:
            return db.query(Estimate).filter(Estimate.id == estimate_id).one_or_none()
        except Exception:
            raise

    def add_estimate(self, estimates: Estimate, db: Session) -> Estimate:
        try:
            db.add(estimates)
            db.commit()
            db.refresh(estimates)
            return estimates
        except Exception:
            db.rollback()
            raise

    def update_estimate(
        self, estimate: Estimate, update_data: EstimateUpdate, db: Session
    ) -> Estimate:
        try:
            for key, value in update_data.dict().items():
                setattr(estimate, key, value)

            db.commit()
            db.refresh(estimate)
            return estimate
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while updating the estimate: {str(e)}",
            )

    def delete_estimate(self, estimate: Estimate, db: Session) -> Estimate:
        try:
            db.delete(estimate)
            db.commit()
            return estimate
        except Exception:
            db.rollback()
            raise
