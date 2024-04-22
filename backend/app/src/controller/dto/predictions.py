import ast
from datetime import datetime

from pydantic import BaseModel
from src.domain.model.prediction import Prediction


class LoadModelResponse(BaseModel):
    ok: bool


class LoadedModelResponse(BaseModel):
    name: str


class BBOXResponse(BaseModel):
    height: int
    left: int
    top: int
    width: int


class DetectionResponse(BaseModel):
    box: BBOXResponse
    class_name: str
    confidence: float


class PredictionResponse(BaseModel):
    id: str
    video_id: str
    model_name: str
    image_path: str
    confidence: float
    iou: float
    detection_list: list[DetectionResponse]
    created_at: datetime

    @staticmethod
    def from_domain(prediction: Prediction) -> "PredictionResponse":
        detection_list = [
            DetectionResponse.parse_obj(obj=ast.literal_eval(detection))
            for detection in prediction.detection_list
        ]
        return PredictionResponse(
            id=str(prediction.id),
            video_id=str(prediction.video_id),
            model_name=prediction.model_name,
            image_path=prediction.image_path,
            confidence=prediction.confidence,
            iou=prediction.iou,
            detection_list=detection_list,
            created_at=prediction.created_at,
        )
