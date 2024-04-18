import uuid
from typing import Optional

from src.domain.model.prediction import Prediction
from src.utils.api_exceptions import ServerErrorException


class PredictionRepository:
    def __init__(self, session):
        self.session = session

    def create_prediction(self, prediction: Prediction) -> Prediction:
        try:
            self.session.add(prediction)
            self.session.commit()
            self.session.refresh(prediction)
        except Exception as ex:
            self.session.rollback()
            raise ServerErrorException(extra=f"Failed to create prediction: {str(ex)}")
        return prediction

    def read_predictions(
        self,
        video_id: Optional[str] = None,
        sort_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[Prediction]:
        try:
            statement = self.session.query(Prediction)
            if video_id:
                statement = statement.filter(Prediction.video_id == uuid.UUID(video_id))
            if sort_type == "asc":
                statement = statement.order_by(Prediction.created_at.asc())
            if sort_type == "desc":
                statement = statement.order_by(Prediction.created_at.desc())
            if limit:
                statement = statement.limit(limit=limit)
            return statement.all()
        except Exception as ex:
            raise ServerErrorException(
                extra=f"Failed to retrieve predictions with video_id={video_id}, "
                f"sort_type={sort_type} and limit={limit}: {str(ex)}"
            )
