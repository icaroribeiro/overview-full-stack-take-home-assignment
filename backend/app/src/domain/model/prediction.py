from sqlalchemy import ARRAY, Column, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin
from src.domain.model import Default
from src.infrastructure.database import Base


class Prediction(Default, Base, SerializerMixin):
    __tablename__ = "prediction"

    video_id = Column("video_id", UUID(as_uuid=True), unique=True, nullable=False)
    image_path = Column("image_path", String, nullable=False)
    model_name = Column("model_name", String, nullable=False)
    confidence = Column("confidence", Float, nullable=False)
    iou = Column("iou", Float, nullable=False)
    detection_list = Column("detection_list", ARRAY(String), nullable=False)
