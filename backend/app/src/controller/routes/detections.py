from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask_restx import Namespace, Resource, fields
from src import AppContainer
from src.controller.dto.health_check_response import HealthCheckResponse
from src.service.detection import DetectionService
from src.service.health_check import HealthCheckService
from src.utils.api_exceptions import ServerErrorException
from src.utils.json_response import respond_with_json

api = Namespace(name="detections", description="Detections related operations")

detection_request_fields = api.model(
    "DetectionRequest",
    {
        "image_path": fields.String(),
        "confidence": fields.Float(),
        "iou": fields.Float(),
    },
)

box_response_fields = api.model(
    name="BoxResponse",
    model={
        "left": fields.Integer(),
        "top": fields.Integer(),
        "width": fields.Integer(),
        "height": fields.Integer(),
    },
)

prediction_response_fields = api.model(
    name="PredictionResponse",
    model={
        "box": fields.Nested(box_response_fields),
        "class_name": fields.String(),
        "confidence": fields.Float(),
    },
)

detection_response_fields = api.model(
    name="DetectionResponse",
    model={
        "id": fields.String(),
        "image_path": fields.String(),
        "confidence": fields.Float(),
        "iou": fields.Float(),
        "model": fields.String(),
        "prediction": fields.List(fields.Nested(prediction_response_fields)),
        "created_at": fields.Date(),
    },
)

detection_collection_response_fields = [detection_response_fields]

detection_error_response_fields = api.model(
    name="DetectionErrorResponse",
    model={"message": fields.String(), "extra": fields.String()},
)


detection_collection_error_response_fields = api.model(
    name="DetectionCollectionErrorResponse",
    model={"message": fields.String(), "extra": fields.String()},
)


@api.route("")
class Detections(Resource):
    @inject
    def __init__(
        self,
        api=None,
        service: DetectionService = Provide[AppContainer.service.detection_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.__service = service

    @api.doc("make_detection")
    @api.response(
        code=HTTPStatus.OK.value, model=detection_response_fields, description="OK"
    )
    def post(self):
        self.__service.make_detection("", 0, 0)
