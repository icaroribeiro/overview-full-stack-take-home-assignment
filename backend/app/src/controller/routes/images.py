from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import request
from flask_restx import Namespace, Resource, fields
from src import AppContainer
from src.controller.dto.images import UploadImageResponse
from src.service.image import ImageService
from src.utils.api_exceptions import NoContentException
from src.utils.json_response import respond_with_json

api = Namespace(name="images", description="Images related operations")


upload_image_response_fields = api.model(
    "UploadImageResponse", {"path": fields.String()}
)

upload_image_error_response_fields = api.model(
    "UploadImageErrorResponse", {"message": fields.String(), "extra": fields.String()}
)


@api.route("/upload")
class UploadImage(Resource):
    @inject
    def __init__(
        self,
        api=None,
        service: ImageService = Provide[AppContainer.service.image_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.__service = service

    @api.response(code=200, model=upload_image_response_fields, description="OK")
    def post(self):
        if "file" not in request.files:
            raise NoContentException(
                extra="The request performed without the file part"
            )

        file = request.files["file"]

        image_path = self.__service.save_image(file=file)

        payload = UploadImageResponse(path=image_path)
        return respond_with_json(payload=payload, code=HTTPStatus.OK.value)
