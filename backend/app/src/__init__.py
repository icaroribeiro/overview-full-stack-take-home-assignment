from flask import Flask
from src.controller import blueprint as endpoints


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["RESTX_MASK_SWAGGER"] = False
    app.config["ERROR_INCLUDE_MESSAGE"] = False
    app.register_blueprint(blueprint=endpoints)
    return app
