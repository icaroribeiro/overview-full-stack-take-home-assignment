from flask import Blueprint
from flask_restx import Api
from src.controller.routes.health_check import namespace as health_check_namespace

blueprint = Blueprint("api", __name__, url_prefix="")


api = Api(
    blueprint,
    title="Overview Take Home Assignment",
    version="1.0",
    description="A REST API developed using Python, Flask framework, Postgres database and Docker container.",
    contact_url="https://www.linkedin.com/in/icaroribeiro",
    contact_email="icaroribeiro@hotmail.com",
    doc="/apidoc",
)

api.add_namespace(health_check_namespace)
