import json
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask_restx import Namespace, Resource, fields, reqparse
from src import AppContainer
from src.controller.dto.predictions import (
    LoadedModelResponse,
    LoadModelResponse,
    PredictionResponse,
)
from src.service.prediction import PredictionService
from src.utils.json_response import respond_with_json
from src.utils.type_validations import int_range

api = Namespace(name="predictions", description="Predictions related operations")

load_model_parser = reqparse.RequestParser()
load_model_parser.add_argument("name", location="json", type=str, required=True)

create_prediction_parser = reqparse.RequestParser()
create_prediction_parser.add_argument(
    "video_id", location="json", type=str, required=True
)
create_prediction_parser.add_argument(
    "image_path", location="json", type=str, required=True
)
create_prediction_parser.add_argument(
    "confidence", location="json", type=float, required=True
)
create_prediction_parser.add_argument("iou", location="json", type=float, required=True)

get_predictions_parser = reqparse.RequestParser()
get_predictions_parser.add_argument(
    "video_id",
    location="args",
    type=str,
    help="If defined, it returns the predictions associated to the video images",
    required=False,
)
get_predictions_parser.add_argument(
    "sort_type",
    location="args",
    type=str,
    choices=("asc", "desc"),
    help="If defined, it returns predictions in an orderly fashion",
    required=False,
)
get_predictions_parser.add_argument(
    "limit",
    location="args",
    type=int_range(min=1, max=10),
    help="If defined, it returns limited amount of predictions. It must be greater than 1 and less than 10",
    required=False,
)


load_model_response_fields = api.model(
    "LoadModelResponse",
    {
        "ok": fields.Boolean(),
    },
)
load_model_error_response_fields = api.model(
    "LoadModelErrorResponse",
    {"message": fields.String(), "extra": fields.String()},
)

loaded_model_response_fields = api.model(
    "LoadedModelResponse",
    {
        "name": fields.String(),
    },
)
loaded_model_error_response_fields = api.model(
    "LoadedModelErrorResponse",
    {"message": fields.String(), "extra": fields.String()},
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

detection_response_fields = api.model(
    name="DetectionResponse",
    model={
        "box": fields.Nested(box_response_fields),
        "class_name": fields.String(),
        "confidence": fields.Float(),
    },
)

prediction_response_fields = api.model(
    name="PredictionResponse",
    model={
        "id": fields.String(),
        "video_id": fields.String(),
        "image_path": fields.String(),
        "model_name": fields.String(),
        "confidence": fields.Float(),
        "iou": fields.Float(),
        "detection_list": fields.List(fields.Nested(detection_response_fields)),
        "created_at": fields.Date(),
    },
)
prediction_error_response_fields = api.model(
    name="PredictionErrorResponse",
    model={"message": fields.String(), "extra": fields.String()},
)
predictions_response_fields = [prediction_response_fields]
predictions_error_response_fields = api.model(
    name="PredictionsErrorResponse",
    model={"message": fields.String(), "extra": fields.String()},
)


@api.route("/load-model")
class LoadModel(Resource):
    @inject
    def __init__(
        self,
        api=None,
        prediction_service: PredictionService = Provide[
            AppContainer.service.prediction_service
        ],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.prediction_service = prediction_service

    @api.doc("load_model")
    @api.expect(load_model_parser)
    @api.response(
        code=HTTPStatus.OK.value, model=load_model_response_fields, description="OK"
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=load_model_error_response_fields,
        description="Internal Server Error",
    )
    def post(self):
        args = load_model_parser.parse_args()
        name = args.get("name")

        self.prediction_service.load_model(name=name)

        return respond_with_json(
            payload=LoadModelResponse(ok=True).json(),
            code=HTTPStatus.OK.value,
        )


@api.route("/get-loaded-model")
class GetLoadedModel(Resource):
    @inject
    def __init__(
        self,
        api=None,
        prediction_service: PredictionService = Provide[
            AppContainer.service.prediction_service
        ],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.prediction_service = prediction_service

    @api.doc("get_loaded_model")
    @api.response(
        code=HTTPStatus.OK.value,
        model=loaded_model_response_fields,
        description="OK",
    )
    @api.response(
        code=HTTPStatus.NO_CONTENT.value,
        model=loaded_model_error_response_fields,
        description="No Content",
    )
    def get(self):
        model = self.prediction_service.get_loaded_model()

        return respond_with_json(
            payload=LoadedModelResponse(name=model.model_name).json(),
            code=HTTPStatus.OK.value,
        )


@api.route("")
class Predictions(Resource):
    @inject
    def __init__(
        self,
        api=None,
        prediction_service: PredictionService = Provide[
            AppContainer.service.prediction_service
        ],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.prediction_service = prediction_service

    @api.doc("create_prediction")
    @api.expect(create_prediction_parser)
    @api.response(
        code=HTTPStatus.CREATED.value,
        model=prediction_response_fields,
        description="Created",
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=prediction_error_response_fields,
        description="Internal Server Error",
    )
    def post(self):
        args = create_prediction_parser.parse_args()
        video_id = args.get("video_id")
        image_path = args.get("image_path")
        confidence = args.get("confidence")
        iou = args.get("iou")

        prediction = self.prediction_service.save_prediction(
            video_id=video_id, image_path=image_path, confidence=confidence, iou=iou
        )

        return respond_with_json(
            payload=PredictionResponse.from_domain(prediction=prediction).json(),
            code=HTTPStatus.CREATED.value,
        )

    @api.doc("get_predictions")
    @api.expect(get_predictions_parser)
    @api.response(
        code=HTTPStatus.OK.value,
        model=predictions_response_fields,
        description="OK",
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=predictions_error_response_fields,
        description="Internal Server Error",
    )
    def get(self):
        args = get_predictions_parser.parse_args()
        video_id = args.get("video_id")
        sort_type = args.get("sort_type")
        limit = args.get("limit")

        prediction_list = self.prediction_service.retrieve_predictions(
            video_id=video_id,
            sort_type=sort_type,
            limit=limit,
        )

        return respond_with_json(
            payload=[
                json.loads(PredictionResponse.from_domain(prediction=prediction).json())
                for prediction in prediction_list
            ],
            code=HTTPStatus.OK.value,
        )
