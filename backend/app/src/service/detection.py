from PIL import Image
from src.domain.model.prediction import Prediction


class DetectionService:
    @staticmethod
    def make_detection(
        image_path: str, confidence: float, iou: float
    ) -> list[Prediction]:
        with open(image_path, "rb") as f:
            original_image = Image.open(f).convert("RGB")
        print(original_image)
        return []
