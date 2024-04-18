from typing import Any

from flask import Response, make_response


def respond_with_json(payload: Any, code: int) -> Response:
    headers = dict()
    headers["Content-Type"] = "application/json"
    return make_response(payload, code, headers)
