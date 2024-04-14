from flask_restx import Namespace, Resource, fields
from src.controller.dto.health_check_response import HealthCheckResponse
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
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @namespace.response(code=200, model=health_check_response_fields, description="OK")
    @namespace.response(
        code=500,
        model=health_check_error_response_fields,
        description="Internal Server Error",
    )
    def get(self):
        response = HealthCheckResponse(ok=True)
        return respond_with_json(payload=response, status_code=200)
