from typing import Optional

from PIL import Image
from src.domain.model.prediction import Prediction
from src.infrastructure.repository.prediction import PredictionRepository
from src.utils.api_exceptions import ServerErrorException
from src.utils.model import Model


class PredictionService:
    def __init__(self, prediction_repository: PredictionRepository):
        self.prediction_repository = prediction_repository

    @staticmethod
    def load_model(name: str) -> Model:
        try:
            global model
            model = Model(model_name=name)
        except Exception as ex:
            raise ServerErrorException(
                extra=f"Failed to load model with name={name}: {str(ex)}"
            )

        return model

    @staticmethod
    def get_loaded_model() -> Model:
        try:
            return model
        except Exception as ex:
            raise ServerErrorException(
                extra="Failed to get loaded model: no model loaded"
            )

    def save_prediction(
        self, video_id: str, image_path: str, confidence: float, iou: float
    ) -> Prediction:
        try:
            with open(image_path, "rb") as f:
                original_image = Image.open(f).convert("RGB")
        except Exception as ex:
            raise ServerErrorException(
                extra=f"Failed to open image={image_path}: {str(ex)}"
            )

        try:
            detection_list = [
                str(prediction.to_dict())
                for prediction in model(original_image, confidence, iou)
            ]
        except Exception as ex:
            raise ServerErrorException(
                extra=f"Failed to create detection list: {str(ex)}"
            )

        prediction = Prediction()
        prediction.video_id = video_id
        prediction.image_path = image_path
        prediction.model_name = model.model_name
        prediction.confidence = confidence
        prediction.iou = iou
        prediction.detection_list = detection_list

        return self.prediction_repository.create_prediction(prediction=prediction)

    def retrieve_predictions(
        self,
        video_id: Optional[str] = None,
        sort_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[Prediction]:
        return self.prediction_repository.read_predictions(
            video_id=video_id,
            sort_type=sort_type,
            limit=limit,
        )
