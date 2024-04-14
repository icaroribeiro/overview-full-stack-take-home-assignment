from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    ok: bool
