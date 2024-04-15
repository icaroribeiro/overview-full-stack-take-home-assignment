from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import make_response, request
from flask_restx import Namespace, Resource, fields
from src import AppContainer
from src.controller.dto.models import GetModelResponse, SetModelResponse
from src.service.model import ModelService
from src.utils.api_exceptions import ServerErrorException
from src.utils.json_response import respond_with_json

api = Namespace(name="models", description="Models related operations")

set_model_request_fields = api.model(
    "SetModelRequest",
    {
        "name": fields.String(),
    },
)

set_model_response_fields = api.model(
    "SetModelResponse",
    {
        "ok": fields.Boolean(),
    },
)

set_model_error_response_fields = api.model(
    "SetModelErrorResponse",
    {"message": fields.String(), "extra": fields.String()},
)

get_model_response_fields = api.model(
    "GetModelResponse",
    {
        "name": fields.String(),
    },
)


@api.route("/set")
class SetModel(Resource):
    @inject
    def __init__(
        self,
        api=None,
        service: ModelService = Provide[AppContainer.service.model_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.__service = service

    @api.doc("set_model")
    @api.response(code=200, model=set_model_response_fields, description="OK")
    @api.response(
        code=500,
        model=set_model_error_response_fields,
        description="Internal Server Error",
    )
    def post(self):
        data = request.json
        try:
            name = data.get("name")
            self.__service.set_model(name=name)
        except Exception as ex:
            raise ServerErrorException(code=404, extra=f"{str(ex)}")

        return respond_with_json(
            payload=SetModelResponse(ok=True), code=HTTPStatus.OK.value
        )


@api.route("/get")
class GetModel(Resource):
    @inject
    def __init__(
        self,
        api=None,
        service: ModelService = Provide[AppContainer.service.model_service],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.__service = service

    @api.doc("get_model")
    @api.response(
        code=HTTPStatus.OK.value, model=get_model_response_fields, description="OK"
    )
    @api.response(
        code=HTTPStatus.NO_CONTENT.value,
        description="NO CONTENT",
    )
    def get(self):
        model = self.__service.get_model()

        if not model:
            return make_response("", HTTPStatus.NO_CONTENT.value)

        return respond_with_json(
            payload=GetModelResponse(name=model.model_name),
            code=HTTPStatus.OK.value,
        )
