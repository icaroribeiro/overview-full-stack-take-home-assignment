from flask import Blueprint
from flask_restx import Api
from src.controller.routes.health_check import api as health_check_namespace
from src.controller.routes.predictions import api as predictions_namespace
from src.controller.routes.videos import api as videos_namespace

blueprint = Blueprint("api", __name__, url_prefix="")


api_description = "A REST API developed using Python, Flask, Postgres and Docker for serving the AI model's predictions"

api = Api(
    blueprint,
    title="Ícaro Ribeiro's Overview Take-Home Assignment",
    version="1.0",
    description=api_description,
    contact_url="https://www.linkedin.com/in/icaroribeiro",
    contact_email="icaroribeiro@hotmail.com",
    doc="/apidoc",
)

api.add_namespace(health_check_namespace)
api.add_namespace(videos_namespace)
api.add_namespace(predictions_namespace)
