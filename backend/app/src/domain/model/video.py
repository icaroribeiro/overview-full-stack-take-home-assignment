from sqlalchemy import ARRAY, Column, String
from sqlalchemy_serializer import SerializerMixin
from src.domain.model import Default
from src.infrastructure.database import Base


class Video(Default, Base, SerializerMixin):
    __tablename__ = "video"

    name = Column("name", String, nullable=False)
    image_path_list = Column("image_path_list", ARRAY(String), nullable=True)
