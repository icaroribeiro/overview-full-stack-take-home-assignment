from typing import Optional

from src.domain.model.video import Video
from src.infrastructure.repository.video import VideoRepository


class VideoService:
    def __init__(
        self,
        video_repository: VideoRepository,
    ):
        self.video_repository = video_repository

    def save_video(self, name: str) -> Video:
        video = Video()
        video.name = name

        return self.video_repository.create_video(video=video)

    def retrieve_videos(self, name: Optional[str] = None) -> list[Video]:
        return self.video_repository.read_videos(name=name)

    def renew_image_path_list(self, id: str, image_path: str) -> Video:
        return self.video_repository.update_image_path_list(
            id=id, image_path=image_path
        )
