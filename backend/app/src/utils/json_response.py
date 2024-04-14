import json

from flask import Response, make_response
from pydantic import BaseModel


def respond_with_json(payload: BaseModel, status_code: int) -> Response:
    return make_response(json.loads(payload.model_dump_json()), status_code)
