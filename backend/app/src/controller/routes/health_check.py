from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response, jsonify, make_response
from flask_restx import Namespace, Resource, fields
from src import AppContainer
from src.controller.dto.health_check_response import HealthCheckResponse
from src.service.health_check import HealthCheckService
from src.utils.json_response import respond_with_json

api = Namespace(name="health-check", description="Health check related operations")


health_check_response_fields = api.model(
    "HealthCheckResponse", {"ok": fields.Boolean()}
)

health_check_error_response_fields = api.model(
    "HealthCheckErrorResponse", {"message": fields.String(), "extra": fields.String()}
)


@api.route("")
class HealthCheck(Resource):
    @inject
    def __init__(
        self,
        api=None,
        service: HealthCheckService = Provide[
            AppContainer.service.health_check_service
        ],
        *args,
        **kwargs,
    ):
        super().__init__(api, *args, **kwargs)
        self.__service = service

    @api.doc("health_check")
    @api.response(
        code=HTTPStatus.OK.value, model=health_check_response_fields, description="OK"
    )
    @api.response(
        code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        model=health_check_error_response_fields,
        description="Internal Server Error",
    )
    def get(self):
        self.__service.check_health()

        return respond_with_json(
            payload=HealthCheckResponse(ok=True).json(), code=HTTPStatus.OK.value
        )
