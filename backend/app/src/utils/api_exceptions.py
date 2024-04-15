from http import HTTPStatus

from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    def __init__(self, message: str, extra: str, code: int):
        super().__init__()
        rv = {"message": message}
        if extra:
            rv["extra"] = extra
        self.data = rv
        self.code = code


class NoContentException(ApiException):
    def __init__(
        self, message=None, extra=None, code: int = HTTPStatus.NO_CONTENT.value
    ):
        super().__init__(message=message, extra=extra, code=code)


class BadRequestException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Bad request",
        extra=None,
        code: int = HTTPStatus.BAD_REQUEST.value,
    ):
        super().__init__(message=message, extra=extra, code=code)


class ServerErrorException(ApiException):
    def __init__(
        self,
        message: str = "Oops! Something went wrong",
        extra: str = None,
        code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value,
    ):
        super().__init__(extra=extra, message=message, code=code)
