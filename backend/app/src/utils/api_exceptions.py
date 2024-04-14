from http import HTTPStatus

from src.utils.json_response import respond_with_json
from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    def __init__(self, message: str, extra: str, code: int):
        super().__init__()
        rv = {"message": message}
        if extra:
            rv["extra"] = extra
        self.__data = rv
        self.__code = code


class ServerErrorException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Something went wrong",
        extra: str = None,
        code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super().__init__(extra=extra, message=message, code=code)
