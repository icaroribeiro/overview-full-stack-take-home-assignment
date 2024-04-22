from datetime import datetime

from pydantic import BaseModel
from src.domain.model.video import Video


class VideoResponse(BaseModel):
    id: str
    name: str
    image_path_list: list[str]
    created_at: datetime

    @staticmethod
    def from_domain(video: Video) -> "VideoResponse":
        image_path_list = (
            [str(image_path) for image_path in video.image_path_list]
            if video.image_path_list
            else []
        )
        return VideoResponse(
            id=str(video.id),
            name=video.name,
            image_path_list=image_path_list,
            created_at=video.created_at,
        )


class UploadImageResponse(BaseModel):
    path: str
