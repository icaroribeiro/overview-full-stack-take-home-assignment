from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask_restx import Namespace, Resource, fields
from src import AppContainer
from src.controller.dto.health_check_response import HealthCheckResponse
from src.service.health_check import HealthCheckService
from src.utils.api_exceptions import ServerErrorException
from src.utils.json_response import respond_with_json

namespace = Namespace(
    name="health-check", description="Health check related operations"
)


health_check_response_fields = namespace.model(
    "HealthCheckResponse", {"ok": fields.Boolean()}
)

health_check_error_response_fields = namespace.model(
    "HealthCheckErrorResponse", {"message": fields.String(), "extra": fields.String()}
)


@namespace.route("")
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

    @namespace.response(code=200, model=health_check_response_fields, description="OK")
    @namespace.response(
        code=500,
        model=health_check_error_response_fields,
        description="Internal Server Error",
    )
    def get(self):
        try:
            is_healthy = self.__service.check_health()
        except Exception as ex:
            raise ServerErrorException(
                extra="The application isn't ready to work as expected"
            )

        if is_healthy:
            payload = HealthCheckResponse(ok=True)
            return respond_with_json(payload=payload, status_code=HTTPStatus.OK)

        payload = HealthCheckResponse(ok=False)
        return respond_with_json(payload=payload, status_code=HTTPStatus.OK)
