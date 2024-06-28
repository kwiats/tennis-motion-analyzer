from sqlalchemy.orm import Session

from src.estimates.models import Estimate


class EstimatesRepository:
    def get_estimates(self, db: Session):
        try:
            return db.query(Estimate).all()
        except Exception:
            raise

    def add_estimate(self, estimates, db: Session):
        try:
            db.add(estimates)
            db.commit()
            db.refresh(estimates)
            return estimates
        except Exception:
            db.rollback()
            raise

    def delete_estimate(self, estimate_id, db: Session):
        try:
            estimate = db.query(Estimate).filter(Estimate.id == estimate_id).one()
            db.delete(estimate)
            db.commit()
            return estimate
        except Exception:
            db.rollback()
            raise
