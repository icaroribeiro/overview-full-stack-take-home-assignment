from pydantic import BaseModel


class DetectionRequest(BaseModel):
    image_path: str


class DetectionResponse(BaseModel):
    ok: bool
