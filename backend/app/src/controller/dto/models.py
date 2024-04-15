from pydantic import BaseModel


class SetModelRequest(BaseModel):
    name: str


class SetModelResponse(BaseModel):
    ok: bool


class GetModelResponse(BaseModel):
    name: str
