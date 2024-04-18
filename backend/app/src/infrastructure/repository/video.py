import uuid
from typing import Optional

from src.domain.model.video import Video
from src.utils.api_exceptions import ServerErrorException


class VideoRepository:
    def __init__(self, session):
        self.session = session

    def create_video(self, video: Video) -> Video:
        try:
            self.session.add(video)
            self.session.commit()
            self.session.refresh(video)
        except Exception as ex:
            self.session.rollback()
            raise ServerErrorException(extra=f"Failed to create video: {str(ex)}")

        return video

    def read_videos(self, name: Optional[str] = None) -> Video:
        statement = self.session.query(Video)

        if name:
            statement = statement.filter(Video.name == name)

        return statement.all()

    def update_image_path_list(self, id: str, image_path: str) -> Video:
        try:
            video = self.session.query(Video).filter(Video.id == uuid.UUID(id)).first()

            if video.image_path_list and (image_path not in video.image_path_list):
                video.image_path_list.append(image_path)
            else:
                video.image_path_list = [image_path]

            self.session.query(Video).filter(Video.id == uuid.UUID(id)).update(
                {Video.image_path_list: video.image_path_list},
            )
            self.session.commit()
            self.session.refresh(video)
        except Exception as ex:
            self.session.rollback()
            raise ServerErrorException(
                extra=f"Failed to update video image list: {str(ex)}"
            )
        return video
